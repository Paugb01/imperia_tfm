import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import csv
import logging

class ParseCSV(beam.DoFn):
    def __init__(self):
        self.headers = None

    def process(self, element):
        for row in csv.reader([element]):
            if self.headers is None:
                self.headers = row
                continue  # Skip the header row

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

def run_pipeline(project, region, bucket):
    # Pipeline options
    pipeline_options = {
        'project': project,
        'region': region,
        'runner': 'DataflowRunner',
        'temp_location': f'gs://{bucket}/tmp',
        'staging_location':  f'gs://{bucket}/staging',
        'save_main_session': True  # This option is key
    }

    # Create pipeline options from the dictionary
    options = PipelineOptions.from_dictionary(pipeline_options)
    options.view_as(beam.options.pipeline_options.StandardOptions).streaming = False

    # Define the pipeline
    with beam.Pipeline(options=options) as p:
        (p
         | 'ReadFromGCS' >> beam.io.ReadFromText(f'gs://{bucket}/historico_ventas.csv')
         | 'ParseCSV' >> beam.ParDo(ParseCSV())
         | 'WriteToBigQuery' >> beam.io.WriteToBigQuery(
                table=f'{project}.tfm_dataset.historico_ventas',
                schema='Id_Producto:STRING, Cliente:STRING, Punto_de_Venta:STRING, Fecha:DATE, Ventas:FLOAT',
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
            )
        )

