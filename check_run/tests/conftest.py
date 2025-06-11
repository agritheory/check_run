# Copyright (c) 2025, AgriTheory and contributors
# For license information, please see license.txt

from pathlib import Path
from unittest.mock import MagicMock, patch

import frappe
import pytest
from frappe.utils import get_bench_path


def _get_logger(*args, **kwargs):
	from frappe.utils.logger import get_logger

	return get_logger(
		module=None,
		with_more_info=False,
		allow_site=True,
		filter=None,
		max_size=100_000,
		file_count=20,
		stream_only=True,
	)


@pytest.fixture(scope="module")
def monkeymodule():
	with pytest.MonkeyPatch.context() as mp:
		yield mp


@pytest.fixture(scope="session", autouse=True)
def db_instance():
	frappe.logger = _get_logger

	currentsite = "test_site"
	sites = Path(get_bench_path()) / "sites"
	if (sites / "currentsite.txt").is_file():
		currentsite = (sites / "currentsite.txt").read_text()

	frappe.init(site=currentsite, sites_path=sites)
	frappe.connect()
	frappe.db.commit = MagicMock()
	yield frappe.db


@pytest.fixture(autouse=True)
def mock_assets_json():
	app_path = Path(frappe.get_app_path("frappe"))
	site_path = Path(frappe.utils.get_site_path())

	def get_abs_path(rel_path):
		if rel_path.startswith("/"):
			return site_path / "public" / rel_path.lstrip("/")
		else:
			return app_path / "public" / rel_path

	mock_assets = {
		"print.bundle.css": str(get_abs_path("css/print.css")),
		"website.bundle.css": str(get_abs_path("css/website.css")),
		"frappe.bundle.js": str(get_abs_path("js/frappe.js")),
		"web_form.bundle.js": str(get_abs_path("js/web_form.js")),
		"desk.bundle.js": str(get_abs_path("js/desk.js")),
		"list.bundle.js": str(get_abs_path("js/list.js")),
		"form.bundle.js": str(get_abs_path("js/form.js")),
		"controls.bundle.js": str(get_abs_path("js/controls.js")),
		"dialog.bundle.js": str(get_abs_path("js/dialog.js")),
	}

	with patch("frappe.utils.get_assets_json", return_value=mock_assets):
		yield
