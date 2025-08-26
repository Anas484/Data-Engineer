from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from data_producer import send_product
from data_consumer import consume_and_store_products
import time

default_args = {
    "owner": "anas",
    "depends_on_past": False,
    "start_date": datetime(2025, 6, 29),
    "email": ["qwerty@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}


def run_producer_for_15_minutes():
    end_time = time.time() + 15 * 60
    while time.time() < end_time:
        send_product()
        time.sleep(1)

def run_consumer_for_15_minutes():
    end_time = time.time() + 15 * 60
    while time.time() < end_time:
        consume_and_store_products()
        time.sleep(1)

with DAG(
    dag_id="api_kafka_postgres",
    default_args=default_args,
    description="My_pipeline",
    schedule="*/30 * * * *",  # Run DAG every 30 minutes
    catchup=False,
    max_active_runs=1,
) as dag:

    produce_data = PythonOperator(
        task_id="Producing_data",
        python_callable=run_producer_for_15_minutes,
        execution_timeout=timedelta(minutes=16)  # buffer
    )

    to_postgres = PythonOperator(
        task_id="Sending_to_postgres",
        python_callable=run_consumer_for_15_minutes,
        execution_timeout=timedelta(minutes=16)
    )

