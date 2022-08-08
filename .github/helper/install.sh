#!/bin/bash

set -e

cd ~ || exit

pip install frappe-bench

bench init frappe-bench --skip-assets --python "$(which python)" --frappe-path "${GITHUB_WORKSPACE}"

cd ./frappe-bench || exit

sed -i 's/^watch:/# watch:/g' Procfile
sed -i 's/^schedule:/# schedule:/g' Procfile

sed -i 's/^socketio:/# socketio:/g' Procfile;
sed -i 's/^redis_socketio:/# redis_socketio:/g' Procfile;

bench setup requirements --node;

bench start &
bench --site test_site reinstall --yes