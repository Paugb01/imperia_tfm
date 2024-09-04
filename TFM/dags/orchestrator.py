from airflow import DAG
from airflow.providers.google.cloud.operators.dataflow import DataflowStartFlexTemplateOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import os
from airflow.models import Variable

# Fetch Airflow Variables
bucket = Variable.get('bucket')
region = Variable.get('region')
project = Variable.get('project')
service_account = Variable.get('service_account')

# Define file path
csv_file_path = '../DatosPrueba/historico_ventas.csv'

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'run_flex_template_pipeline',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['tfm'],
) as dag:

    # Task to upload the CSV to GCS
    upload_file = LocalFilesystemToGCSOperator(
        task_id="upload_file",
        src=csv_file_path,
        dst='historico_ventas.csv',
        bucket=bucket,
    )
    # Task to start the Dataflow Flex Template job
    run_flex_template = DataflowStartFlexTemplateOperator(
        task_id="run_flex_template_pipeline",
        body={
            'launchParameter': {
                'jobName': 'flex-template-job',
                'containerSpecGcsPath': f'gs://{bucket}/flex_templates/template_spec.json',
                'parameters': {
                    'inputFile': f'gs://{bucket}/historico_ventas.csv',
                    'outputTable': f'{project}:tfm_dataset.historico_ventas',
                },
                'environment': {
                    'serviceAccountEmail': service_account,
                    'tempLocation': f'gs://{bucket}/tmp'
                }
            }
        },
        location=region,
        project_id=project
    )

    # Define task dependencies
    upload_file >> run_flex_template
