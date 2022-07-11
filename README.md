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
### Testing
#### Running Cypress tests
To set up local Cypress tests;
```bash
cd apps/check_run
yarn
```
Additional steps may be required on WSL, use Nicky's guide:
https://nickymeuleman.netlify.app/blog/gui-on-wsl2-cypress

```bash
yarn run cypress open
```