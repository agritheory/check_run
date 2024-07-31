# Formatos de impresión de ejemplo: verificación de comprobante y resumen de referencias

Para aprovechar la funcionalidad de impresión de cheques de Check Run, deberá configurar un formato de impresión en ERPNext. Con la aplicación se proporciona un formato de impresión de cheque de ejemplo para que sirva como punto de partida. Los formatos de impresión son tan únicos como las organizaciones que utilizan ERPNext, por lo que la plantilla de ejemplo debe personalizarse para satisfacer sus necesidades. Está habilitado de forma predeterminada y se puede encontrar en la lista Formato de impresión.

![Captura de pantalla que muestra la pantalla de vista previa de impresión de una ejecución de verificación que aplica el formato de impresión de comprobante de ejemplo. La mitad superior del formato incluye los datos reales del cheque y la mitad inferior incluye las referencias asociadas con el pago.](./assets/print_format_example_voucher.png)

También se proporciona un segundo formato de impresión llamado Formato de impresión secundario de ejemplo en Formatos de impresión. No está diseñado para imprimir cheques, pero mostrará un resumen de las referencias asociadas con cada cheque.

![Captura de pantalla que muestra la vista previa de impresión de una ejecución de verificación que aplica el formato de impresión secundario de ejemplo. Muestra una tabla de referencias y montos asociados al pago.](./assets/print_format_secondary.png)

Ambos formatos de impresión de ejemplo están configurados para mostrar solo transacciones en las que el Modo de pago está incluido en el campo de selección múltiple Modos de pago imprimibles en Ejecución de cheque que se encuentra en Configuración de ejecución de cheque.

Una consideración a tener en cuenta si incluye referencias en el formato de impresión (como los ejemplos) es que si hay muchas referencias asociadas con un pago, la lista puede exceder la longitud del documento y no imprimirse correctamente. El valor de Número de facturas por comprobante en Configuración de ejecución de cheques limitará el número de referencias asociadas con un pago y se puede ajustar según sea necesario.

Recursos adicionales:

- [Documentación del formato de impresión de ERPNext](https://docs.erpnext.com/docs/v14/user/manual/en/customize-erpnext/print-format)

