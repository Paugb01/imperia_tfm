from airflow import DAG
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.google.cloud.operators.dataflow import DataflowTemplatedJobStartOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from airflow.models import Variable

# Fetch Airflow Variables
bucket_source = Variable.get('bucket_source')  # Source bucket
bucket = Variable.get('bucket')  # Destination bucket
region = Variable.get('region')
project = Variable.get('project')
service_account = Variable.get('service_account')

# Define folder paths in GCS
source_folder_path = 'assets/'  # Folder in source bucket
source_file_path = f'{source_folder_path}historico_ventas.csv'
destination_file_path = f'{bucket}/{source_folder_path}historico_ventas.csv'

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
    'upload_transform_load',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['tfm'],
) as dag:

    # Task to check for the existence of the file in the source bucket
    check_file_existence = GCSObjectExistenceSensor(
        task_id='check_file_existence',
        bucket=bucket_source,
        object=source_file_path,
        google_cloud_conn_id='google_cloud_default'  # Default connection ID 
    )
    
    # Task to start the Dataflow Flex Template job
    start_template_job = DataflowTemplatedJobStartOperator(
        task_id="start_template_job",
        project_id=project,
        template="gs://dataflow-templates-europe-southwest1/latest/GCS_CSV_to_BigQuery",
        parameters={"inputFilePattern": f"{destination_file_path}", 
                    "schemaJSONPath": f"{bucket}/{source_folder_path}schema.json",
                    "outputTable": "pakotinaikos.tfm_dataset.historico_ventas_testing",
                    "bigQueryLoadingTemporaryDirectory": f"{bucket}/tmp",
                    "badRecordsOutputTable": "pakotinaikos.tfm_dataset.BadRecords",
                    "delimiter": ",",
                    "csvFormat": "Default",
                    "containsHeaders": "true"},
        location=region,
        wait_until_finished=True,
    )


    # Define task dependencies
check_file_existence >> start_template_job

