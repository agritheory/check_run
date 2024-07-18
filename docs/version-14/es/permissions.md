# Permisos y flujo de trabajo predeterminados

Se recomienda encarecidamente que establezca permisos del sistema para limitar qué usuarios pueden ver y ejecutar una ejecución de verificación. El único permiso que aplica la aplicación es que un usuario debe tener un nivel de permiso en ERPNext para crear entradas de pago para poder realizar una ejecución de verificación. Además, solo el primer usuario que acceda a un borrador del tipo de documento Check Run puede editarlo. 

Consulte la [página de documentación de ERPNext](https://docs.erpnext.com/docs/v13/user/manual/en/setting-up/users-and-permissions) para obtener más información sobre los permisos de usuarios y roles.

## Solo primer usuario
El tipo de documento Check Run solo permite que un único usuario interactúe con él a la vez. El primer usuario con permiso de escritura en la ejecución de verificación específica puede editar, los espectadores posteriores no. 

## Solo se permite una ejecución de verificación de borrador
Solo se permite una ejecución de cheque en borrador por combinación de cuenta bancaria/pagable. Esto tiene como objetivo minimizar el doble pago de facturas.

## Permisos de rol
Fuera de la caja, la ejecución de cheques tiene el mismo permiso que la entrada de pagos. Para la mayoría de las organizaciones pequeñas esto puede estar bien, pero las organizaciones más grandes con políticas de aprobación de documentos y el deseo de limitar el acceso de las personas a cheques impresos probablemente querrán implementar políticas adicionales. Las políticas de impresión de ejecución de cheques y generación de ACH se basan en permisos para el ingreso de pagos, no en la ejecución de cheques en sí.


