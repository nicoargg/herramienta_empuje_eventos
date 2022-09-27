# Herramienta Sodimac
una pequeña herramienta para automatizar el envio de stock y cobertura

Primeros pasos:
- Inicializar el entorno de python e instalar las dependencias en el archivo "requirements.txt"
- Crear el archivo .env y rellenarlo con las creedenciales de la Base de datos que deseamos acceder:
#### USER=
#### PASS=
#### HOST=
#### PORT=
#### SERVICE_NAME=

Para realizar el envio de stock y cobertura debemos:

- Pegar los sku necesarios en el archivo: "sku_list.txt" con el formato: <br>
258582X <br>
2429456 <br>
5395234 <br>

- Ejecutar el archivo "bdd_connect.py"

Para eliminar los eventos antiguos de los sku pegados en el archivo "sku_list.txt":
- Ejecutar el archivo "delete_events.py"
