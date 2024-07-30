# The DAG object; we'll need this to instantiate a DAG
from airflow.models.dag import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
import textwrap
from datetime import datetime, timedelta

abs_path_pipeline = '/Users/paugarciabardisa/projects/imperia_tfm/TFM/pipeline.py'

with DAG(
    'run_beam_pipeline',
    default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    },
    description="A simple tutorial DAG",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["tfm"],
) as dag:


    # Task to run the Apache Beam pipeline
    t1 = BashOperator(
        task_id='run_beam_pipeline',
        bash_command=f'python {abs_path_pipeline}',
        dag=dag,
    )


