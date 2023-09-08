## Check Run

### License

MIT

### Production Installation Instructions

See the [installation guide](./docs/installationguide.md) for detailed instructions for either a production or development environment.

#### Developer Setup

First, set up a new bench and substitute a path to the python version to use. Python should be 3.10 latest for V14. These instructions use [pyenv](https://github.com/pyenv/pyenv) for managing environments.
```shell
# Version 14
bench init --frappe-branch version-14 {{ bench name }} --python ~/.pyenv/versions/3.10.3/bin/python3
```

Create a new site in that bench
```shell
cd {{ bench name }}
bench new-site {{ site name }} --force --db-name {{ site name }}
```

Download the ERPNext app
```shell
# Version 14
bench get-app erpnext --branch version-14
bench get-app hrms --branch version-14
```

Download the Time and Expense application
```shell
bench get-app check_run https://github.com/agritheory/check_run
```

Install the apps to your site
```shell
bench --site {{ site name }} install-app erpnext hrms check_run

# Optional: Check that all apps installed on your site
bench --site {{ site name }} list-apps
```

Set developer mode in `site_config.json`
```shell
nano sites/{{ site name }}/site_config.json
# Add this line:
  "developer_mode": 1,

```
Install pre-commit:
```
# ~/frappe-bench/apps/check_run/
pre-commit install
```

Add the site to your computer's hosts file to be able to access it via: `http://{{ site name }}:[8000]`. You'll need to enter your root password to allow your command line application to make edits to this file.
```shell
bench --site {{site name}} add-to-hosts
```

Launch your bench (note you should be using Node.js v14 for a Version 13 bench and Node.js v16 for a Version 14 bench)
```shell
bench start
```

Optional: install a [demo Company and its data](./exampledata.md) to test the Electronic Payments module's functionality
```shell
bench execute 'check_run.tests.setup.before_test'
```

To run `mypy` locally:
```shell
source env/bin/activate
mypy ./apps/check_run/check_run --ignore-missing-imports
```