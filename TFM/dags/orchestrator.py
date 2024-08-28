from airflow import DAG
from airflow.providers.google.cloud.operators.dataflow import DataflowStartFlexTemplateOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
bucket = os.getenv("BUCKET")
region = os.getenv("REGION")
project = os.getenv("PROJECT_ID")
service_account = os.getenv("SERVICE_ACCOUNT_EMAIL", "default-service-account@your-project.iam.gserviceaccount.com")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'run_flex_template_pipeline',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['tfm'],
) as dag:

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
