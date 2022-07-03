## Check Run



#### License

MIT

## Install Instructions
To install this app in a production environemnt 


### Developer setup
Set up a new bench, substitute a path to the python version to use, which should 3.8 latest for V13 and 3.10 latest for V14. These instructions use pyenv for managing environments. 

```
bench init --frappe-branch version-13 {{ bench name }} --python ~/.pyenv/versions/3.8.12/bin/python3
```
For version 14
```
bench init --frappe-branch version-14 {{ bench name }} --python ~/.pyenv/versions/3.10.3/bin/python3
```

Create a new site in that bench
```
cd {{ bench name }}
bench new-site {{ site name }} --force --db-name {{ site name }}
```
Download the ERPNext app
```
bench get-app erpnext --branch version-13
```
Download this application
```
bench get-app check_run git@github.com:agritheory/check_run.git 
```

Set developer mode in `site_config.json`
```
cd {{ site name }}
nano site_config.json
# 
 "developer_mode": 1
```

Restore the database
```
mysql -u root -p {{ site name }} < {{data base file path}}.sql
```
Set a new password for the local Administrator that is not the same as the production Administrator password 
```
bench set-admin-password {{local password}}
```

Migrate, build and get the site ready
```
bench start
```
In a new terminal window
```
bench update
```

### Printer Server setup
```
sudo apt-get install gcc cups python3-dev libcups2-dev -y
bench pip install pycups
sudo usermod -a -G lpadmin {username} # the "frappe" user in most installations
```
Go to `{server URL or localhost}:631` to access the CUPS web interface
Configuration on a remote server will take extra steps to secure:
https://askubuntu.com/questions/23936/how-do-you-administer-cups-remotely-using-the-web-interface

