# Uso de los datos de ejemplo para experimentar con la ejecución de verificación

La aplicación Check Run viene con un script `test_setup.py` cuyo uso es completamente opcional. Si ejecuta el script, llena su sitio ERPNext con datos comerciales de demostración para una empresa ficticia llamada Chelsea Fruit Co. Los datos le permiten experimentar y probar la funcionalidad de la aplicación Check Run antes de instalar la aplicación en su sitio ERPNext.

Se recomienda instalar los datos de demostración en su propio sitio para evitar posibles interferencias con la configuración o los datos en el sitio ERPNext de su organización.

Con `bench start` ejecutándose en segundo plano, ejecute el siguiente comando para instalar los datos de demostración:


```shell
bench execute 'check_run.test_setup.before_test'
# to reinstall from scratch and setup test data
bench reinstall --yes --admin-password admin --mariadb-root-password admin && bench execute 'check_run.tests.setup.before_test'
```

Consulte la [guía de instalación] (./installationguide.md) para obtener instrucciones detalladas sobre cómo configurar un banco, un nuevo sitio e instalar ERPNext y la aplicación Check Run.

