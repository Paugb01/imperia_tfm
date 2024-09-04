from airflow import DAG
from airflow.providers.google.cloud.operators.gcs import GCSSynchronizeBucketsOperator
from airflow.providers.google.cloud.operators.dataflow import DataflowStartFlexTemplateOperator
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
destination_folder_path = 'assets/'  # Folder in destination bucket
source_file_path = f'{source_folder_path}historico_ventas.csv'
destination_file_path = f'gs://{bucket}/{destination_folder_path}historico_ventas.csv'

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

    # Task to synchronize (copy) the contents of the source folder to the destination folder
    synchronize_folders = GCSSynchronizeBucketsOperator(
        task_id='synchronize_folders',
        source_bucket=bucket_source,
        destination_bucket=bucket,
        source_object=source_folder_path,  # Root sync directory in source bucket
        destination_object=destination_folder_path,  # Root sync directory in destination bucket
        recursive=True,  # To include subdirectories
        allow_overwrite=True,  # Allow overwriting files in the destination bucket
        delete_extra_files=False  # Optional: Set to True if you want to delete files in the destination bucket not present in the source bucket
    )
    
    # Task to start the Dataflow Flex Template job
    run_flex_template = DataflowStartFlexTemplateOperator(
        task_id='run_flex_template_pipeline',
        body={
            'launchParameter': {
                'jobName': 'flex-template-job',
                'containerSpecGcsPath': f'gs://{bucket}/flex_templates/template_spec.json',
                'parameters': {
                    'inputFile': destination_file_path,  # Path to the file in the destination folder
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
    synchronize_folders >> run_flex_template
