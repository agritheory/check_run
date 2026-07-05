#!/bin/bash

export PIP_ROOT_USER_ACTION=ignore
export CI=Yes

set -e

DB="${DB:-mariadb}"

cd ~ || exit

sudo apt-get update
sudo apt-get remove -y mysql-server mysql-client || true
sudo apt-get install -y libcups2-dev redis-server mariadb-client

if [ "$DB" = "postgres" ]; then
	sudo apt-get install -y postgresql-client libpq-dev
fi

pip install --upgrade pip
pip install frappe-bench

if [ "$DB" = "mariadb" ]; then
	mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "SET GLOBAL character_set_server = 'utf8mb4'"
	mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "SET GLOBAL collation_server = 'utf8mb4_unicode_ci'"
	mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "CREATE DATABASE IF NOT EXISTS test_site"
	mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "CREATE USER IF NOT EXISTS 'test_site'@'localhost' IDENTIFIED BY 'test_site'"
	mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "GRANT ALL PRIVILEGES ON \`test_site\`.* TO 'test_site'@'localhost'"
	mariadb --host 127.0.0.1 --port 3306 -u root -proot -e "FLUSH PRIVILEGES"
	SITE_CONFIG="${GITHUB_WORKSPACE}/.github/helper/site_config.json"
elif [ "$DB" = "postgres" ]; then
	PGPASSWORD=travis psql -h 127.0.0.1 -U postgres -c "CREATE USER test_site WITH PASSWORD 'test_site';" || true
	PGPASSWORD=travis psql -h 127.0.0.1 -U postgres -c "CREATE DATABASE test_site OWNER test_site;" || true
	SITE_CONFIG="${GITHUB_WORKSPACE}/.github/helper/site_config_postgres.json"
else
	echo "Unsupported DB: ${DB}"
	exit 1
fi

echo "BRANCH_NAME: ${BRANCH_NAME}"
echo "DB: ${DB}"
git clone https://github.com/frappe/frappe --branch "${BRANCH_NAME}"
bench init frappe-bench --frappe-path ~/frappe --python "$(which python)" --skip-assets --ignore-exist

mkdir -p ~/frappe-bench/sites/test_site
cp "${SITE_CONFIG}" ~/frappe-bench/sites/test_site/site_config.json

install_whktml() {
	wget -q -O /tmp/wkhtmltox.tar.xz https://github.com/frappe/wkhtmltopdf/raw/master/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz
	tar -xf /tmp/wkhtmltox.tar.xz -C /tmp
	sudo mv /tmp/wkhtmltox/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf
	sudo chmod o+x /usr/local/bin/wkhtmltopdf
}
install_whktml &

cd ~/frappe-bench || exit

sed -i 's/watch:/# watch:/g' Procfile
sed -i 's/schedule:/# schedule:/g' Procfile
sed -i 's/socketio:/# socketio:/g' Procfile
sed -i 's/redis_socketio:/# redis_socketio:/g' Procfile

bench get-app erpnext https://github.com/frappe/erpnext --branch "${BRANCH_NAME}" --resolve-deps --skip-assets
bench get-app hrms https://github.com/frappe/hrms --branch "${BRANCH_NAME}" --skip-assets
bench get-app check_run "${GITHUB_WORKSPACE}" --skip-assets

printf '%s\n' 'frappe' 'erpnext' 'hrms' 'check_run' > ~/frappe-bench/sites/apps.txt
bench setup requirements --python
bench setup requirements --dev
bench use test_site

bench start &> bench_run_logs.txt &
CI=Yes bench build --app frappe &

bench --site test_site reinstall --yes --admin-password admin

echo "BENCH VERSION NUMBERS:"
bench version
echo "SITE LIST-APPS:"
bench list-apps
