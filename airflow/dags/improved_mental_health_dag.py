import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from scripts.mental_health_service import (
    _load_quote,
    _load_image,
    _create_content_image,
    _send_to_teams
)

with DAG(
    dag_id="improved_mental_health_dag",
    start_date=pendulum.datetime(2024, 6, 17, tz="UTC"),
    schedule_interval="0 10 * * *",
    catchup=False,
    tags=["msi_6", "daily_mental_service"]
) as dag:

    start_op = EmptyOperator(task_id="start")

    load_quote_op = PythonOperator(
        task_id="load_quote",
        python_callable=_load_quote
    )

    load_image_op = PythonOperator(
        task_id="load_image",
        python_callable=_load_image
    )

    create_content_image_op = PythonOperator(
        task_id="create_content_image",
        python_callable=_create_content_image
    )

    send_to_teams_op = PythonOperator(
        task_id="send_to_teams",
        python_callable=_send_to_teams
    )

    finish_op = EmptyOperator(task_id="finish")

    start_op >> [load_quote_op, load_image_op] >> create_content_image_op >> send_to_teams_op >> finish_op
