#!/bin/bash

set -e

cd ~ || exit

pip install frappe-bench
git clone https://github.com/frappe/frappe --branch version-13 --depth 1
bench init --skip-assets --frappe-path ~/frappe --python "$(which python)" frappe-bench

mkdir ~/frappe-bench/sites/test_site
cp -r "${GITHUB_WORKSPACE}/.github/helper/site_config.json" ~/frappe-bench/sites/test_site

mysql --host 127.0.0.1 --port 3306 -u root -e "SET GLOBAL character_set_server = 'utf8mb4'"
mysql --host 127.0.0.1 --port 3306 -u root -e "SET GLOBAL collation_server = 'utf8mb4_unicode_ci'"

mysql --host 127.0.0.1 --port 3306 -u root -e "CREATE USER 'test_frappe'@'localhost' IDENTIFIED BY 'test_frappe'"
mysql --host 127.0.0.1 --port 3306 -u root -e "CREATE DATABASE test_frappe"
mysql --host 127.0.0.1 --port 3306 -u root -e "GRANT ALL PRIVILEGES ON \`test_frappe\`.* TO 'test_frappe'@'localhost'"

mysql --host 127.0.0.1 --port 3306 -u root -e "UPDATE mysql.user SET Password=PASSWORD('travis') WHERE User='root'"
mysql --host 127.0.0.1 --port 3306 -u root -e "FLUSH PRIVILEGES"

cd ./frappe-bench || exit

sed -i 's/^watch:/# watch:/g' Procfile
sed -i 's/^schedule:/# schedule:/g' Procfile

sed -i 's/^socketio:/# socketio:/g' Procfile;
sed -i 's/^redis_socketio:/# redis_socketio:/g' Procfile;

bench setup requirements --node

cd ./apps/frappe || exit
yarn add node-sass@4.13.1
cd ../..

bench get-app erpnext --branch version-13
bench get-app check_run "${GITHUB_WORKSPACE}"

bench install-app check_run erpnext

bench start &> bench_run_logs.txt &
bench --site test_site reinstall --yes
CI=Yes bench build

bench restart 
