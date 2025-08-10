from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
import sys
from docker.types import Mount


sys.path.append('/opt/airflow/api_request')

from insert_record import main, export_csv

def example_function():
    print("This is an example task in the Airflow DAG.")
    

default_args = {
    'description': 'Weather Data Orchestrator DAG',
    'start_date': datetime(2025, 7, 24),
    'catchup': False,
    }

dag = DAG(
    dag_id='weather_data_dbt_orchestrator',
    default_args=default_args,
    schedule = timedelta(minutes=5),
)

with dag:
    task1 = PythonOperator(
        task_id='weather_data_ingestion',
        python_callable=main
    )
    
    task2 = DockerOperator(
        task_id='transform_data_task',
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command='run',
        working_dir='/usr/app',
        mounts=[
            Mount(source='/Users/aveg/Desktop/Work/Weather ELT/dbt/my_project', target='/usr/app', type='bind'),
            # Mount(source='/Users/aveg/Desktop/Work/Weather ELT/dbt', target='/root/.dbt', type='bind'),
            Mount(source='/Users/aveg/Desktop/Work/Weather ELT/dbt/.dbt', target='/root/.dbt', type='bind'),

        ],
        network_mode='weatherelt_my-network',
        docker_url='unix://var/run/docker.sock',
        auto_remove='success',
        mount_tmp_dir=False
    )
    
    task3 = PythonOperator(
        task_id='export_for_visualization',
        python_callable= export_csv
    )
    

    task1 >> task2 >> task3