from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import subprocess
import os

# Definir argumentos por defecto del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definir el DAG
dag = DAG(
    'beam_dataflow_pipeline',
    default_args=default_args,
    description='Run Apache Beam pipeline on Dataflow',
    schedule_interval='@monthly',
)

# Definir la función que ejecutará el pipeline
def run_beam_pipeline():
    # Path to the beam pipeline script
    pipeline_script = '/path/to/pipeline.py'
    subprocess.run(['python3', pipeline_script], check=True)

# Definir la tarea de Airflow
run_pipeline = PythonOperator(
    task_id='run_beam_pipeline',
    python_callable=run_beam_pipeline,
    dag=dag,
)

# Establecer la secuencia de tareas
run_pipeline
