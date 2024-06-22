import datetime

import pendulum
from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy import DummyOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.operators.python import PythonOperator
from airflow.utils.trigger_rule import TriggerRule

from scripts.mental_health_service import (
    _load_quote,
    _load_image,
    _create_content_image,
    _send_to_teams
)


def check_date():
    holidays = Variable.get("HOLIDAYS", deserialize_json=True)
    current_date = datetime.datetime.now().strftime("%d.%m")
    if current_date in holidays:
        return "skip_message"
    else:
        return ["load_quote", "load_image"]


with DAG(
    dag_id="scheduled_mental_health_dag",
    start_date=pendulum.datetime(2024, 6, 18, tz="UTC"),
    schedule_interval="0 10 * * *",
    catchup=False,
    tags=["msi_7", "daily_mental_service"]
) as dag:

    start_op = EmptyOperator(task_id="start")

    check_date_op = BranchPythonOperator(
        task_id="check_date",
        python_callable=check_date
    )

    skip_message_op = DummyOperator(
        task_id="skip_message"
    )

    load_quote_op = PythonOperator(
        task_id="load_quote",
        python_callable=_load_quote,
    )

    load_image_op = PythonOperator(
        task_id="load_image",
        python_callable=_load_image,
    )

    create_content_image_op = PythonOperator(
        task_id="create_content_image",
        python_callable=_create_content_image,
    )

    send_to_teams_op = PythonOperator(
        task_id="send_to_teams",
        python_callable=_send_to_teams
    )

    finish_op = EmptyOperator(
        task_id="finish",
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS
    )

    start_op >> check_date_op >> [load_quote_op, load_image_op] >> create_content_image_op >> send_to_teams_op >> finish_op
    start_op >> check_date_op >> skip_message_op >> finish_op
