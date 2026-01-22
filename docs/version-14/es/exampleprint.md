# Formatos de Impresión de Ejemplo: Cheque de Comprobante y Resumen de Referencias

Para aprovechar la función de impresión de cheques de Check Run, deberá configurar un formato de impresión en ERPNext. La aplicación incluye un formato de impresión de ejemplo de cheque de comprobante como punto de partida. Los formatos de impresión son tan únicos como las organizaciones que utilizan ERPNext, por lo que la plantilla de ejemplo debe personalizarse según sus necesidades. Está habilitada por defecto y se encuentra en la lista de Formatos de Impresión.

![Captura de pantalla que muestra la vista previa de impresión de un Check Run con el formato de impresión de ejemplo de comprobante. La mitad superior del formato incluye los datos del cheque y la mitad inferior, las referencias asociadas al pago.](./assets/print_format_example_voucher.png)

También se incluye un segundo formato de impresión llamado Formato de Impresión Secundario de Ejemplo en la sección Formatos de Impresión. No está diseñado para imprimir cheques, sino que muestra un resumen de las referencias asociadas a cada cheque.

![Captura de pantalla que muestra la vista previa de impresión de una Ejecución de Cheque con el Formato de Impresión Secundario de Ejemplo. Muestra una tabla de referencias e importes asociados al pago.](./assets/print_format_secondary.png)

Ambos formatos de impresión de ejemplo están configurados para mostrar solo las transacciones cuyo Modo de Pago esté incluido en el campo de selección múltiple "Modos de Pago Imprimibles en la Ejecución de Cheque" de la Configuración de la Ejecución de Cheque.

Al incluir referencias en el formato de impresión (como en los ejemplos), tenga en cuenta que si hay muchas referencias asociadas a un pago, la lista podría exceder la longitud del papel y no imprimirse correctamente. El valor de "Número de Facturas por Comprobante" en la Configuración de la Ejecución de Cheque limitará el número de referencias asociadas a un pago y se puede ajustar según sea necesario.

Recursos adicionales:

- [Documentación del formato de impresión de ERPNext](https://docs.erpnext.com/docs/v14/user/manual/en/customize-erpnext/print-format)

