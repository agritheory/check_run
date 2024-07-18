# Verificar Ejecutar guía de instalación

## Configuración del desarrollador
Primero, configure un nuevo banco y sustituya una ruta a la versión de Python para usar. Python debe ser la versión 3.8 más reciente para V13 y la versión 3.10 más reciente para V14. Estas instrucciones utilizan [pyenv](https://github.com/pyenv/pyenv) para administrar entornos.

```shell
# Version 13
bench init --frappe-branch version-13 {{ bench name }} --python ~/.pyenv/versions/3.8.12/bin/python3

# Version 14
bench init --frappe-branch version-14 {{ bench name }} --python ~/.pyenv/versions/3.10.3/bin/python3
```

Crea un nuevo sitio en ese banco.
```shell
cd {{ bench name }}
bench new-site {{ site name }} --force --db-name {{ site name }}
```

Descarga la aplicación ERPNext
```shell
# Version 13
bench get-app erpnext --branch version-13

# Version 14
bench get-app payments
bench get-app erpnext --branch version-14
bench get-app hrms
```

Descargue la aplicación Check Run
```shell
bench get-app check_run git@github.com:agritheory/check_run.git 
```

Instale las aplicaciones en su sitio
```shell
bench --site {{ site name }} install-app erpnext hrms check_run

# Optional: Check that all apps installed on your site
bench --site {{ site name }} list-apps
```

Establecer el modo de desarrollador en `site_config.json`
```shell
nano sites/{{ site name }}/site_config.json
# Add this line:
  "developer_mode": 1,
```

Agregue el sitio al archivo de hosts de su computadora para poder acceder a él a través de: `http://{{ nombre del sitio }}:[8000]`. Deberá ingresar su contraseña de root para permitir que su aplicación de línea de comando edite este archivo.
```shell
bench --site {{site name}} add-to-hosts
```

Inicie su banco (tenga en cuenta que debe usar Node.js v14 para un banco de la versión 13 y Node.js v16 para un banco de la versión 14)
```shell
bench start
```

Opcional: instale una [Empresa de demostración y sus datos] (./exampledata.md) para probar la funcionalidad del módulo Check Run
```shell
bench execute 'check_run.tests.setup.before_test'
```

