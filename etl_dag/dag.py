from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models.baseoperator import chain
from datetime import datetime
from grammy_etl import read_db, transform_db
from spotify_etl import read_csv, transform_csv
from merge_load_store import merge, load, store


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 11),  # Update the start date to today or an appropriate date
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    'workshop_dag',
    default_args=default_args,
    description='Our first DAG with ETL process!',
    schedule_interval='@daily',  # Set the schedule interval as per your requirements
) as dag:

    merge = PythonOperator(
        task_id = 'merge',
        python_callable = merge,
        provide_context = True,
    )

    read_csv = PythonOperator(
        task_id = 'read_csv',
        python_callable = read_csv,
        provide_context = True,
    )

    transform_csv = PythonOperator(
        task_id = 'transform_csv',
        python_callable = transform_csv,
        provide_context = True,
    )

    read_db = PythonOperator(
        task_id = 'read_db',
        python_callable = read_db,
        provide_context = True,
    )

    transform_db = PythonOperator(
        task_id = 'transform_db',
        python_callable = transform_db,
        provide_context = True,
    )

    store = PythonOperator(
        task_id='store',
        python_callable = store,
        provide_context = True,
    )

    load = PythonOperator(
        task_id ='load',
        python_callable = load,
        provide_context = True,
    )

    merge >> load >> store
    read_csv >> transform_csv >> merge
    read_db >> transform_db >> merge