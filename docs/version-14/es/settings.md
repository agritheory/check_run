<!-- Copyright (c) 2025, AgriTheory y colaboradores
Para obtener información sobre la licencia, consulte license.txt-->

# Ajustes de la Ejecución de Cheque

La entrada "Ajustes de la Ejecución de Cheque" determina el comportamiento de una Ejecución de Cheque para una combinación específica de cuenta bancaria/cuenta por pagar. Deberá confirmar ajustes por separado para cada combinación de cuenta bancaria/cuenta por pagar que planee usar en una Ejecución de Cheque.

![Captura de pantalla de la vista de lista de Ajustes de la Ejecución de Cheque con dos entradas: una para la combinación de Banco Local y Nómina por Pagar y otra para la combinación de Banco Local y Cuentas por Pagar.](./assets/SettingsList.png)

Si el sistema no encuentra los ajustes para la combinación de cuentas que está usando en una Ejecución de Cheque iniciada, lo redirigirá automáticamente a la página de ajustes para confirmar las opciones. También puede acceder directamente a la lista de ajustes buscando "Lista de Ajustes de la Ejecución de Cheque" en AwesomeBar y haciendo clic en el botón "Añadir Ajustes de la Ejecución de Cheque".

![Captura de pantalla que muestra la parte superior de la configuración predeterminada para una combinación de cuenta bancaria y cuenta por pagar. A continuación, se incluye una descripción de cada configuración y su valor predeterminado.](./assets/Settings_Main.png)

- **Rol del aprobador:**
- Si las ejecuciones de cheques requieren la aprobación de otro usuario, se debe indicar su rol aquí.

```mermaid
graph TD
  A[Draft] -- Send for Approval --> B[Pending Approval]
  A -- Save --> A
  B -- Approve --> C[Approved]
  B -- Revert to draft --> A
  C -- Revert to Draft --> A
  C -- Process Check Run --> D[Submitting]
  D -- On Error --> A
  D --> E[Submitted]
  D --> F[Ready to Print]
```

- **Incluir facturas de compra:**
- Seleccionado por defecto
- Indica si las facturas de compra se incluyen en una ejecución de cheques. Consulte a continuación para obtener más información y algunas consideraciones sobre las facturas de compra con un calendario de pagos definido.
- **Incluir asientos de diario:**
- Seleccionado por defecto
- Indica si los asientos de diario se incluyen en una ejecución de cheques. Por ejemplo, los datos de demostración tienen una entrada de diario para los impuestos sobre la nómina adeudados a la autoridad fiscal local. Esto solo se mostrará en una ejecución de cheque si esta opción está seleccionada.
- **Incluir reclamaciones de gastos:**
- Seleccionado por defecto
- Indica si las reclamaciones de gastos se incluyen en una ejecución de cheque.
- Consulte la [página de configuración](./configuration.md) para obtener instrucciones sobre cómo configurar un método de pago, un banco y una cuenta bancaria predeterminados para un "Empleado".
- **Pre-chequear partidas vencidas:**
- No seleccionado por defecto
- Indica si la casilla "Pagar" está preseleccionada para cualquier partida cuya fecha de vencimiento sea anterior a la fecha de contabilización de la ejecución de cheque.
- **Permitir cancelación:**
- No seleccionado por defecto
- Indica si un usuario puede cancelar una ejecución de cheque. Si se selecciona esta opción y un usuario cancela una Ejecución de Cheque, el sistema eliminará la referencia al nombre del documento de la Ejecución de Cheque en todos los asientos de pago realizados mediante la ejecución, pero no cancelará los asientos de pago en sí.
- **Cancelación en Cascada:**
- No seleccionada por defecto (¡no se recomienda seleccionar esta opción!)
- Indica si el sistema cancelará todos los asientos de pago asociados a una Ejecución de Cheque si esta se cancela.
- **Número de Facturas por Comprobante:**
- El valor predeterminado es 0, lo que indica que el sistema no modifica esta configuración y que utilizará 5 facturas por comprobante.
- Esta configuración establece un límite máximo para el número de facturas por parte que se pueden agrupar en cada comprobante para esa parte.
- La siguiente captura de pantalla muestra el resultado de una Ejecución de Cheque enviada con el número de facturas por comprobante establecido en 2. De las cuatro facturas pagadas a Exceptional Grid, se agrupan de modo que dos se pagan con un comprobante y las otras dos con otro.
- Esto también se puede configurar. Por proveedor en el campo "Número de facturas por comprobante de cheque". La configuración por proveedor anula el número en la configuración de la ejecución de cheque.
- **Formato de impresión secundario:**
- Permite que los pagos con más del número de facturas divididas configurado se impriman en cascada en un formato de impresión independiente que detalla todos los documentos vinculados.
- **Dividir facturas por dirección:**
- Si se marca esta opción, se validará si se paga al mismo proveedor a diferentes direcciones y se dividirán los asientos de pago correctamente.
- **Liberar automáticamente facturas en espera:**
- De forma predeterminada, las facturas en espera no se mostrarán si su fecha de liberación no está dentro del período de la ejecución de cheque. La casilla de verificación permite que las facturas en espera se liberen y paguen automáticamente en la ejecución de cheque.
- **Establecer fecha de contabilización de la entrada de pago:**
- De forma predeterminada, la ejecución de cheque utilizará la fecha de hoy para determinar la contabilización en las entradas de pago. Al cambiar esta configuración, puede retroceder o adelantar la fecha. La fecha de referencia en la Entrada de Pago siempre utiliza la fecha de contabilización de la Ejecución de Cheque. Cualquiera de estos campos se puede utilizar en sus formatos de impresión personalizados.

![Tabla de resultados de la Ejecución de Cheque que muestra una fila con ocho facturas pagadas (dos para AgriTheory, dos para Cooperative Ag Finance y cuatro para Exceptional Grid). Las dos primeras facturas de Exceptional Grid tienen el número de referencia de cheque ACC-PAY-2022-00003 y el siguiente conjunto de dos facturas tiene el número de referencia de cheque ACC-PAY-2022-00004. Se dividieron en comprobantes diferentes debido a que la configuración limitaba a dos facturas por comprobante.](./assets/VoucherGroup.png)

La sección Configuración de Impresión abarca las opciones de impresión.

![Captura de pantalla que muestra la sección Configuración de impresión.](./assets/settings_print_section.png)

- **Vista previa de impresión:**
- El valor predeterminado es "Generar PDF automáticamente después del envío". Sin embargo, la opción "Imprimir desde la vista previa de impresión" permite ver e imprimir con diferentes formatos de impresión.
- **Formato de impresión:**
- Enlace a un formato de impresión predeterminado preferido.
- **Formato de impresión secundario:**
- Enlace a un formato de impresión de respaldo.
- **Modos de pago imprimibles en la ejecución de cheques:**
- Conjunto de los modos de pago que se deben imprimir. Como se detalla en la página de configuración, esto debe incluir los modos de pago con el tipo "Banco". Para ver cómo se usa esto en un formato de impresión, consulte el código del [Comprobante de ejemplo](./exampleprint.md) incluido en la ejecución de cheque, que solo procesa los pagos con una forma de pago incluida en esta lista.
- **Formatos de cheque con imagen de fondo:**
- La opción "Predeterminado" no está seleccionada; si está marcada, permite al usuario cargar una imagen de fondo para aplicarla en la vista previa de impresión (consulte el código del [Comprobante de ejemplo](./exampleprint.md) para saber cómo se usa).

La siguiente sección de configuración permite configurar una forma de pago predeterminada opcional para facturas de compra, informes de gastos y asientos de diario. Si no se especifica una forma de pago en la factura de compra, el informe de gastos o el asiento de diario, ni se ha definido una predeterminada para la parte (consulte la página [Configuración](./configuration.md) para obtener más información), este campo se utiliza para rellenar la columna "Forma de pago" en la ejecución de cheque.

![Captura de pantalla que muestra la sección "Modo de pago predeterminado" en la configuración.](./assets/Settings_MOP.png)

También hay una sección para todas las configuraciones relacionadas con los pagos ACH.

![Captura de pantalla que muestra la sección "Configuración de ACH". A continuación, se detalla la descripción de cada configuración y su valor predeterminado.](./assets/Settings_ACH.png)

- **Extensión de archivo ACH:**
- El valor predeterminado es "ach"
- Una ejecución de cheque genera automáticamente un archivo ACH si alguna de las opciones de Modo de pago utilizadas es "Electrónica". Esta configuración es un campo de texto que indica la extensión de archivo que el sistema utilizará al crear estos archivos. Su institución bancaria podría requerir una extensión específica.
- Consulte la [página de configuración](./configuration.md) para obtener instrucciones sobre cómo indicar que un "Modo de Pago" es una transferencia bancaria electrónica.
- **Código de Clase de Servicio ACH:**
- El valor predeterminado es 200
- Las opciones incluyen 200 (débitos y créditos combinados), 220 (solo créditos) y 225 (solo débitos). Este valor es obligatorio para los campos del archivo ACH y debe reflejar la naturaleza de sus pagos mediante transferencia bancaria electrónica.
- **Código de Clase Estándar ACH:**
- El valor predeterminado es PPD (Entrada de Pago y Depósito Preacordado)
- PPD es el único código de clase de entrada estándar admitido actualmente.
- **Descripción ACH:**
- El valor predeterminado está en blanco
- Campo opcional para agregar una descripción a los archivos ACH.

La sección Configuración de Pago Positivo permite al usuario adjuntar automáticamente los resultados del [Informe de Pago Positivo](./positivepay.md) como un archivo CSV o Excel a la Ejecución de Cheque. Las opciones son similares a las que el usuario vería en el cuadro de diálogo de exportación del informe.

![Captura de pantalla que muestra la sección Configuración de Positive Pay. A continuación, se incluye una descripción de cada configuración y su valor predeterminado.](./assets/Settings_Positive_Pay.png)

- **Generar y adjuntar automáticamente Positive Pay a la ejecución del cheque:**
- No seleccionado por defecto
- Indica si los resultados del informe de Positive Pay se adjuntan a la ejecución del cheque. El informe requiere una cuenta bancaria y las fechas de inicio y fin para filtrar los resultados. Esta función utiliza la cuenta bancaria y la fecha de contabilización de la ejecución de cheque para dichas entradas.
- **Formato de archivo de pago positivo:**
- El valor predeterminado es "CSV"
- "CSV" o "Excel" indica el formato del informe adjunto a la ejecución de cheque.
- **Delimitador CSV:**
- El valor predeterminado es una coma (solo relevante si se selecciona "CSV" como formato de archivo).
- Un solo carácter para usar como delimitador de campo en el archivo CSV resultante.
- **Comillas CSV:**
- El valor predeterminado es "No numérico" (solo relevante si se selecciona "CSV" como formato de archivo).
- Indica el comportamiento de las comillas en los valores de campo (si se usan). Dado que una columna del informe corresponde al nombre de la parte, se recomienda usar algún tipo de comillas entre los valores si existe la posibilidad de que el nombre de la parte incluya el carácter delimitador.

## Consideraciones para facturas de compra con calendarios de pago

Una característica de la ejecución de cheques para facturas de compra con un calendario de pago definido es que desglosa y muestra transacciones separadas para cada plazo de pago pendiente del calendario de pago por fecha de vencimiento, en lugar del importe total de la factura.

El siguiente ejemplo asume una factura de compra por un alquiler de equipo de $30,000 a 18 meses que se paga mediante un calendario de pago en 18 cuotas mensuales iguales.

![Captura de pantalla de las transacciones de una ejecución de cheques para Tireless Equipment Rental, Inc. desde principios de año hasta mayo. Muestra transacciones separadas para cada mes por $1,666.67 cada una, lo que refleja los pagos mensuales vencidos en el Calendario de Pagos.](./assets/PaymentScheduleTransactions.png)

La Ejecución de Cheques aprovecha el mecanismo integrado de ERPNext, que actualiza automáticamente el Calendario de Pagos de una factura cuando una Entrada de Pago se vincula a una Condición de Pago en el calendario. Hay algunas suposiciones y consideraciones de ERPNext que se deben tener en cuenta al configurar los Calendarios de Pagos o al realizar Entradas de Pago en ellos para garantizar que este mecanismo funcione correctamente, tanto dentro como fuera de una Ejecución de Cheques:

1. Para un Calendario de Pagos de varias filas, cada fila debe vincularse a una Condición de Pago única. Esto actúa como la clave para identificar correctamente la cuota en el Calendario de Pagos que se vincula a la Entrada de Pago y actualizar el calendario en consecuencia.

![Captura de pantalla de un ejemplo de Calendario de Pagos definido en una factura de compra. La columna "Término de Pago" de la tabla enlaza a documentos únicos, como "Cuota de Alquiler 1", "Cuota de Alquiler 2", etc., para las distintas filas.](./assets/InvoicePaymentScheduleExample.png)

2. Si crea una Entrada de Pago fuera de una Ejecución de Cheque, correspondiente a una parte de una factura (para cumplir con una Condición de Pago), existe una validación para verificar y enlazar con la Condición de Pago pendiente más reciente. Si el campo "Término de Pago" de la tabla "Referencias de Pago" se deja en blanco, se intenta completar el campo y se avisa al usuario para que lo revise. Si la Entrada de Pago abarca varias Condiciones de Pago, debe haber una fila para cada parte del pago con un enlace a su respectiva Condición de Pago.

![Captura de pantalla del cuadro de diálogo del formulario al editar una fila en la tabla "Referencias de Pago". El campo "Término de Pago" muestra el valor "Cuota de Alquiler 3" para vincular el importe asignado al plazo correspondiente en el Calendario de Pagos de la factura.