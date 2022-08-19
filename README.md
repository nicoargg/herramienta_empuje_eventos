# automatizacion_sodimac
una pequeña herramienta para automatizar el envio de stock y cobertura

Primeros pasos:
- Inicializar el entorno de python e instalar las dependencias en el archivo "requirements.txt"
- Rellenar los datos de la bdd en el archivo "config.env"

para realizar el envio de stock y cobertura debemos:

- Pegar los sku necesarios en el archivo: "sku_list.txt" con el formato:
258582X
2429456
5395234
- Ejecutar el archivo "bdd_connect.py"


para eliminar elementos antiguos:
- pegar la id de los eventos en el archivo "id_event_list.txt" con el formato:
4425125
5245696
5925953
- Ejecutar el archivo "delete_events.py"
