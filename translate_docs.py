import os
import re
import json
import pathlib
import importlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from google.cloud import translate_v2 as translate
from git import Repo
from github import Github, GithubException


def get_languages():
	app_name = pathlib.Path(__file__).resolve().parent.name
	hooks = importlib.import_module(f"{app_name}.hooks")
	try:
		return hooks.docs_languages
	except Exception:
		return []


def set_google_credentials():
	secret_value = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
	with open("credentials.json", "w") as f:
		json.dump(json.loads(secret_value), f)
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"


def get_pull_request_number():
	github_ref = os.getenv("GITHUB_REF")
	match = re.match(r"refs/pull/(\d+)/merge", github_ref)
	return int(match.group(1)) if match else None


def translate_file(source_file, target_file, target_language, translate_client):
	translation = translate_client.translate(
		source_file, target_language=target_language, format_="text"
	)
	with open(target_file, "w", encoding="utf-8") as f:
		f.write(translation["translatedText"])


def translate_md_files():
	target_languages = get_languages()

	if not target_languages:
		return

	set_google_credentials()
	translate_client = translate.Client()
	base_branch = os.getenv("GITHUB_BASE_REF", "main")  # Default to 'main' if not available
	repo_name = os.getenv("GITHUB_REPOSITORY")
	g = Github(os.getenv("GITHUB_TOKEN"))

	repo = Repo(search_parent_directories=True)
	origin = repo.remote(name="origin")
	origin.fetch()

	version_folders = [f for f in os.listdir("docs") if os.path.isdir(os.path.join("docs", f))]

	pull_request_number = get_pull_request_number()
	repository = g.get_repo(repo_name, lazy=False)
	pull_request = repository.get_pull(pull_request_number)
	head_branch = pull_request.head.ref
	files = pull_request.get_files()

	modified_files = {}

	for file in files:
		try:
			modified_files[file.filename] = repository.get_contents(
				file.filename, ref=head_branch
			).decoded_content.decode("utf-8")
		except Exception:
			continue

	with ThreadPoolExecutor() as executor:
		futures = []
		for version in version_folders:
			for target_language in target_languages:
				for filename, modified_file in modified_files.items():
					if filename.startswith(f"docs/{version}/en") and filename.endswith(".md"):
						source_file = modified_file
						target_folder = f"docs/{version}/{target_language}"
						target_file = os.path.join(target_folder, os.path.basename(filename))
						if not os.path.exists(target_folder):
							os.makedirs(target_folder)
						futures.append(
							executor.submit(translate_file, source_file, target_file, target_language, translate_client)
						)

		for future in as_completed(futures):
			try:
				future.result()
			except Exception as e:
				print(f"Error during translation: {e}")

	for version in version_folders:
		for target_language in target_languages:
			target_folder = f"docs/{version}/{target_language}"
			branch_name = f"translate-{target_language}"
			repo.git.checkout(base_branch)
			repo.git.checkout("-b", branch_name)
			repo.index.add([target_folder])
			commit_message = f"Translate {target_language}"
			repo.index.commit(commit_message)
			origin.push(branch_name)

			title = f"Translate to {target_language}"
			body = f"This pull request translates to {target_language}"
			try:
				repository.create_pull(title=title, body=body, head=branch_name, base=base_branch)
			except GithubException as e:
				print(f"Failed to create pull request for {target_language}: {e}")


if __name__ == "__main__":
	translate_md_files()
