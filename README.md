# automatizacion_sodimac
una pequeña herramienta para automatizar el envio de stock y cobertura

Primeros pasos:
- Inicializar el entorno de python e instalar las dependencias en el archivo "requirements.txt"
- Crear el archivo .env y rellenarlo con los datos de la bdd:
#### USER=
#### PASS=
#### HOST=
#### PORT=
#### SERVICE_NAME=

para realizar el envio de stock y cobertura debemos:

- Pegar los sku necesarios en el archivo: "sku_list.txt" con el formato:
258582X
2429456
5395234
- Ejecutar el archivo "bdd_connect.py"

Para eliminar los eventos antiguos de los sku pegados en el archivo "sku_list.txt":
- Ejecutar el archivo "delete_events.py"
