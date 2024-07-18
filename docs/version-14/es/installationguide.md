# Verificar Ejecutar guía de instalación

## Configuración del desarrollador
Primero, configure un nuevo banco y sustituya una ruta a la versión de Python para usar. Python debe ser la versión 3.8 más reciente para V13 y la versión 3.10 más reciente para V14. Estas instrucciones utilizan [pyenv](https://github.com/pyenv/pyenv) para administrar entornos.

```cáscara
# Versión 13
inicio del banco --frappe-branch versión-13 {{ nombre del banco }} --python ~/.pyenv/versions/3.8.12/bin/python3

# Versión 14
inicio del banco --frappe-branch versión-14 {{ nombre del banco }} --python ~/.pyenv/versions/3.10.3/bin/python3
```

Crea un nuevo sitio en ese banco.
```cáscara
cd {{ nombre del banco }}
banco nuevo-sitio {{ nombre del sitio }} --force --db-name {{ nombre del sitio }}
```

Descarga la aplicación ERPNext
```cáscara
# Versión 13
banco get-app erpnext --branch versión-13

# Versión 14
pagos de banco de aplicaciones
banco get-app erpnext --branch versión-14
banco get-app hrms
```

Descargue la aplicación Check Run
```cáscara
banco get-app check_run git@github.com:agritheory/check_run.git 
```

Instale las aplicaciones en su sitio
```cáscara
banco --site {{ nombre del sitio }} instalar-aplicación erpnext hrms check_run

# Opcional: Verifique que todas las aplicaciones estén instaladas en su sitio
banco --site {{ nombre del sitio }} lista de aplicaciones
```

Establecer el modo de desarrollador en `site_config.json`
```cáscara
nano sitios/{{ nombre del sitio }}/site_config.json
# Añade esta línea:
  "modo_desarrollador": 1,
```

Agregue el sitio al archivo de hosts de su computadora para poder acceder a él a través de: `http://{{ nombre del sitio }}:[8000]`. Deberá ingresar su contraseña de root para permitir que su aplicación de línea de comando edite este archivo.
```cáscara
banco --site {{nombre del sitio}} agregar a hosts
```

Inicie su banco (tenga en cuenta que debe usar Node.js v14 para un banco de la versión 13 y Node.js v16 para un banco de la versión 14)
```cáscara
inicio en el banco
```

Opcional: instale una [Empresa de demostración y sus datos] (./exampledata.md) para probar la funcionalidad del módulo Check Run
```cáscara
banco ejecuta 'check_run.tests.setup.before_test'
```
