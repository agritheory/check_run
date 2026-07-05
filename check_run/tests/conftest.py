# Copyright (c) 2026, AgriTheory and contributors
# For license information, please see license.txt

import json
import os
from pathlib import Path
from unittest.mock import MagicMock

import frappe
import pytest
from frappe.utils import get_bench_path

BENCH_SITES = Path(get_bench_path()) / "sites"

# Frappe log handlers write to ../logs relative to cwd. Run pytest from
# apps/check_run, so chdir to bench/sites before test modules import erpnext.
os.chdir(BENCH_SITES)


def _get_logger(module=None, *args, **kwargs):
	from frappe.utils.logger import get_logger

	return get_logger(
		module=module,
		with_more_info=False,
		allow_site=True,
		filter=None,
		max_size=100_000,
		file_count=20,
	)


frappe.logger = _get_logger


@pytest.fixture(scope="module")
def monkeymodule():
	with pytest.MonkeyPatch.context() as mp:
		yield mp


@pytest.fixture(scope="session", autouse=True)
def db_instance():
	currentsite = "test_site"
	if (BENCH_SITES / "common_site_config.json").is_file():
		currentsite = json.loads((BENCH_SITES / "common_site_config.json").read_text()).get(
			"default_site"
		)

	frappe.init(site=currentsite, sites_path=BENCH_SITES)

	common_site_config = {}
	if (BENCH_SITES / "common_site_config.json").is_file():
		common_site_config = json.loads((BENCH_SITES / "common_site_config.json").read_text())
	port = common_site_config.get("webserver_port") or common_site_config.get("http_port") or 8000
	if not frappe.conf.host_name:
		frappe.conf.host_name = f"http://127.0.0.1:{port}"
	frappe.connect()
	frappe.db.commit = MagicMock()
	yield frappe.db
