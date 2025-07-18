from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

#  Add the correct path to your scripts folder here
sys.path.append("/home/ubuntu/airflow/scripts")

#  Now import the ETL function
from weather_etl import run_weather_etl

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='weather_to_snowflake_etl',
    default_args=default_args,
    description='ETL weather data to Snowflake',
    schedule_interval=timedelta(minutes=5),#'@daily',  or timedelta(minutes=5)
    start_date=datetime(2023, 1, 1),
    catchup=False
) as dag:

    task = PythonOperator(
        task_id='run_weather_etl',
        python_callable=run_weather_etl
    )
