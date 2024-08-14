from airflow import DAG
from airflow.providers.google.cloud.operators.dataflow import DataflowCreatePythonJobOperator
from airflow.utils.dates import days_ago
import os
from dotenv import load_dotenv

# Set env variables
load_dotenv()
bucket = os.getenv("BUCKET")
region = os.getenv("REGION")
project = os.getenv("PROJECT_ID")
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") # Existe flag para service account en airlfow
abs_path_pipeline = '/Users/paugarciabardisa/projects/imperia_tfm/TFM/pipeline.py'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
}

with DAG(
    'run_beam_pipeline',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['tfm'],
) as dag:

    run_beam = DataflowCreatePythonJobOperator(
        task_id="run_beam_pipeline",
        py_file=f'{abs_path_pipeline}',
        job_name="run_beam_pipeline",
        options={
            'project': f'{project}',
            'region': f'{region}',
            'temp_location': f'gs://{bucket}/tmp',
            'staging_location': f'gs://{bucket}/staging',
            'save_main_session': True,
            'serviceAccountEmail': 'beam-719@pakotinaikos.iam.gserviceaccount.com'
        },
        py_interpreter="python3",
    )
