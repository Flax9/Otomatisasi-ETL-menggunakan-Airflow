from airflow import DAG
from airflow.operators.python import PythonOperator #type: ignore
from datetime import datetime, timedelta
# Import fungsi dari folder utils
from utils.bpom_etl_logic import run_etl_process

default_args = {
    'owner': 'magang_bpom',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='etl_monitoring_bpom_v2_modular',
    default_args=default_args,
    description='Pipeline ETL BPOM - Modular Version',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['bpom', 'modular'],
) as dag:

    # Task ini sekarang memanggil fungsi dari file eksternal
    task_etl = PythonOperator(
        task_id='execute_etl_logic',
        python_callable=run_etl_process
    )

    task_etl