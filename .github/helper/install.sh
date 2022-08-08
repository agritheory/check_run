#!/bin/bash

set -e

cd ~ || exit


pip install frappe-bench

bench init --frappe-branch version-13 --python python3.9 frappe-bench --skip-assets 

cd ./frappe-bench || exit

bench new-site test_site --db-root-password admin --admin-password admin

sed -i 's/^watch:/# watch:/g' Procfile
sed -i 's/^schedule:/# schedule:/g' Procfile

sed -i 's/^socketio:/# socketio:/g' Procfile;
sed -i 's/^redis_socketio:/# redis_socketio:/g' Procfile;

bench setup requirements --node;

bench get-app erpnext --branch version-13 --skip-assets

bench start
