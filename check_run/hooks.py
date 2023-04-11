from . import __version__ as app_version

app_name = "check_run"
app_title = "Check Run"
app_publisher = "AgriTheory"
app_description = "Payables Utilities for ERPNext"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "support@agritheory.dev"
app_license = "MIT"
required_apps = ["erpnext", "hrms"]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/check_run/css/check_run.css"
app_include_js = [
	"check_run.bundle.js",
]

# include js, css files in header of web template
# web_include_css = "/assets/check_run/css/check_run.css"
# web_include_js = "/assets/check_run/js/check_run.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "check_run/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	'Employee': 'public/js/custom/employee_custom.js',
	"Supplier": 'public/js/custom/supplier_custom.js',
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "check_run.install.before_install"
after_install = "check_run.customize.after_install"
after_migrate = 'check_run.customize.load_customizations'

# Uninstallation
# ------------

# before_uninstall = "check_run.uninstall.before_uninstall"
# after_uninstall = "check_run.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "check_run.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Bank": "check_run.overrides.bank.CustomBank"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"check_run.tasks.all"
# 	],
# 	"daily": [
# 		"check_run.tasks.daily"
# 	],
# 	"hourly": [
# 		"check_run.tasks.hourly"
# 	],
# 	"weekly": [
# 		"check_run.tasks.weekly"
# 	]
# 	"monthly": [
# 		"check_run.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "check_run.check_run.doctype.check_run.test_check_run.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "check_run.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "check_run.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------
#

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"check_run.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []

jinja = {
	"methods": [
		"frappe.contacts.doctype.address.address.get_default_address"
	]
}