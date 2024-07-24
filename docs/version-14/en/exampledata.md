# Using the Example Data to Experiment with Check Run

The Check Run application comes with a `test_setup.py` script that is completely optional to use. If you execute the script, it populates your ERPNext site with demo business data for a fictitious company called Chelsea Fruit Co. The data enable you to experiment with and test the Check Run application's functionality before installing the app into your ERPNext site.

It's recommended to install the demo data into its own site to avoid potential interference with the configuration or data in your organization's ERPNext site.

With `bench start` running in the background, run the following command to install the demo data:


```shell
bench execute 'check_run.test_setup.before_test'
# to reinstall from scratch and setup test data
bench reinstall --yes --admin-password admin --mariadb-root-password admin && bench execute 'check_run.tests.setup.before_test'
```

Refer to the [installation guide](./installationguide.md) for detailed instructions for how to set up a bench, a new site, and installing ERPNext and the Check Run application.

