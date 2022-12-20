#!/usr/bin/env python
import pandas as pd
from bokeh.plotting import curdoc
from bokeh.models import ColumnDataSource, TableColumn, DataTable, Div
from bokeh.layouts import column

import pika
import sys
import ssl
import json
import configparser

datos = pd.DataFrame(columns=['id', 'timestamp', 'reliability'])

def push(json_data: dict, df: pd.DataFrame) -> pd.DataFrame:

    """
    Push data to a dataframe
    """

    index = json_data['id']
    timestamp = json_data['timestamp']
    reliability = json_data['payload'][0]['value']

    new_data = pd.DataFrame([index, timestamp, reliability], columns=df.columns)
    # concat the new data to the old data
    datos = pd.concat([df, new_data], ignore_index=True)
    return datos


config = configparser.ConfigParser()

config.read("./config.ini")

LOCALHOST = config["MESSAGEBUS"]["LOCALHOST"]
SERVER = config["MESSAGEBUS"]["SERVER"]
PORT = config["MESSAGEBUS"]["PORT"]
USERNAME = config["MESSAGEBUS"]["USERNAME"]
PASSWORD = config["MESSAGEBUS"]["PASSWORD"]
CA_CERT = config["MESSAGEBUS"]["CA_CERT"]

EXCHANGE = config["MESSAGEBUS"]["EXCHANGE"]
ROUTING_KEY = config["MESSAGEBUS"]["ROUTING_KEY_OUTPUT"]
try:
    if CA_CERT!='':
        context = ssl.create_default_context(cafile=CA_CERT)
        context.check_hostname=False
        context.verify_mode = ssl.VerifyMode.CERT_NONE
        ssl_options = pika.SSLOptions(context, LOCALHOST)
        credentials = pika.PlainCredentials(USERNAME, PASSWORD)
        conn_params = pika.ConnectionParameters(host=SERVER,
                            port=PORT,
                            credentials=credentials,
                                                ssl_options=ssl_options)
    else:
        credentials = pika.PlainCredentials(USERNAME, PASSWORD)
        conn_params = pika.ConnectionParameters(host=SERVER,
                    port=PORT,
                    credentials=credentials)
    connection = pika.BlockingConnection(conn_params)
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise

channel = connection.channel()

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(
    exchange=EXCHANGE, queue=queue_name, routing_key=ROUTING_KEY)

print(f' [*] Waiting for logs in {ROUTING_KEY}. To exit press CTRL+C')


def callback(ch, method, properties, body):
    datos = push(json.loads(json.loads(body)), datos)
    #print(" [x] %r:%r (%r)" % (method.routing_key, body, properties.headers))

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()


def create_datatable(src:ColumnDataSource,
    width:int = 600,  
    height:int = 600, 
    widthColumns:int = 100,
    ) -> DataTable:

    """
    Crea un DataTable con los datos de la fuente de datos   
    """

    columns = []
    columns.append(TableColumn(field="index", title="index", width=widthColumns))
    columns.append(TableColumn(field="timestamp", title="timestamp", width=widthColumns))
    columns.append(TableColumn(field="reliability", title="reliability", width=widthColumns))

    tabla = DataTable(sortable = False, reorderable = False, 
                autosize_mode='none', source=src,
                columns=columns, index_position = None, 
                width = width, height = height)

    return tabla

def update():
    """
    Actualiza el DataTable con los datos nuevos
    """
    tabla.source.data = dict(datos)

tabla = create_datatable(ColumnDataSource(datos))

curdoc().add_root(column(Div(text="""<h1>Resultados en Streaming</h1>""", width=800), tabla, width=800))
curdoc().title = "Aplicación ZDMP"
curdoc().add_periodic_callback(update, 1000 * 15)