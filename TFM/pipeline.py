import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import csv
import logging
import os
from dotenv import load_dotenv

# Set env variables
load_dotenv()
bucket = os.getenv("BUCKET")
region = os.getenv("REGION")
project = os.getenv("PROJECT_ID")
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Set Google Application Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

class ParseCSV(beam.DoFn):
    def __init__(self):
        self.headers = None

    def process(self, element):
        for row in csv.reader([element]):
            if self.headers is None:
                self.headers = row
                continue  # Omite la fila de encabezado

            if len(row) == 5:
                try:
                    yield {
                        'Id_Producto': row[0],
                        'Cliente': row[1],
                        'Punto_de_Venta': row[2],
                        'Fecha': row[3],
                        'Ventas': float(row[4])
                    }
                except ValueError as e:
                    logging.error(f"Could not convert value to float: {row[4]} - Error: {e}")
            else:
                logging.warning(f"Row does not have the expected number of columns: {row}")

def run():
    # Configuración de las opciones del pipeline
    pipeline_options = {
        'project': project,
        'region': region,
        'runner': 'DataflowRunner',
        'temp_location': f'{bucket}/tmp',
        'staging_location':  f'{bucket}/staging',
        'requirements_file': 'requirements.txt',
        'save_main_session': True  # Esta es la opción clave
    }

    # Creación de las opciones del pipeline a partir del diccionario
    options = PipelineOptions.from_dictionary(pipeline_options)
    options.view_as(beam.options.pipeline_options.StandardOptions).streaming = False

    # Definición del pipeline
    with beam.Pipeline(options=options) as p:
        (p
         | 'ReadFromGCS' >> beam.io.ReadFromText( f'{bucket}/historico_ventas.csv')
         | 'ParseCSV' >> beam.ParDo(ParseCSV())
         | 'WriteToBigQuery' >> beam.io.WriteToBigQuery(
                table=f'{project}.tfm_dataset.historico_ventas',
                schema='Id_Producto:STRING, Cliente:STRING, Punto_de_Venta:STRING, Fecha:DATE, Ventas:FLOAT',
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
            )
        )

if __name__ == '__main__':
    run()

