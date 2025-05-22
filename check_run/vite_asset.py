import os
import json

def get_vite_js_bundle():
    manifest_path = os.path.join(
        os.path.dirname(__file__),
        "public", "dist", "js", "manifest.json"
    )
    if not os.path.exists(manifest_path):
        return "check_run_vue.bundle.js"
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    for key, value in manifest.items():
        if value.get("file", "").startswith("check_run_vue"):
            return f"assets/check_run/dist/js/{value['file']}"
