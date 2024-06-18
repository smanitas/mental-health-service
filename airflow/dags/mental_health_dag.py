import json
import logging

import pendulum
import pymsteams
import requests
from airflow import DAG
from airflow.hooks.base import BaseHook
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator


def load_quote(ti):
    api_url = Variable.get("QUOTE_API_URL")
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        quote_data = response.json()
        quote = quote_data.get("content")
        author = quote_data.get("author")
        if quote and author:
            ti.xcom_push(
                key="quote",
                value={
                    "text": quote,
                    "author": author
                }
            )
            logging.info("Quote is successfully loaded")
        else:
            raise ValueError("Failed to load quote")
    except (requests.exceptions.RequestException, ValueError) as e:
        logging.exception(f"Error loading quote: {e}")


def load_image(ti):
    unsplash_conn = BaseHook.get_connection("UNSPLASH_API")
    unsplash_token = json.loads(unsplash_conn.extra)["client_id"]
    api_url = (
            f"https://api.unsplash.com/photos/random"
            f"?query=nature"
            f"&orientation=landscape"
            f"&client_id={unsplash_token}"
    )
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        image_url = response.json()["urls"]["small"]
        if image_url:
            logging.info("Image URL is successfully loaded")
            ti.xcom_push(key="image_url", value=image_url)
        else:
            raise ValueError("Failed to load image URL")
    except (requests.exceptions.RequestException, ValueError) as e:
        logging.exception(f"Error loading image: {e}")


def send_to_teams(**kwargs):
    teams_conn = BaseHook.get_connection("TEAMS_WEBHOOK")
    webhook_url = teams_conn.host

    ti = kwargs["ti"]
    quote = ti.xcom_pull(task_ids="load_quote", key="quote")
    image_url = ti.xcom_pull(task_ids="load_image", key="image_url")
    sender_name = Variable.get("SENDER_NAME")
    logging.debug(f"Using SENDER_NAME: {sender_name}")

    content = (
        f"Sent by {sender_name}\n\n"
        f"Quote: {quote}\n\n"
        f"![Image]({image_url})"
    )

    try:
        teams_message = pymsteams.connectorcard(webhook_url)
        teams_message.text(content)
        teams_message.send()
        logging.info("Content is successfully sent to Teams")
    except pymsteams.TeamsWebhookException as e:
        logging.exception(f"Failed to send content to Teams due to webhook error: {e}")
        raise
    except requests.RequestException as e:
        logging.exception(f"Failed to send content to Teams due to network connectivity issue: {e}")
        raise
    except Exception as e:
        logging.exception(f"An unexpected error occurred while sending content to Teams: {e}")
        raise


with DAG(
    dag_id="mental_health_dag",
    start_date=pendulum.datetime(2024, 6, 10, tz="UTC"),
    schedule_interval="0 10 * * *",
    catchup=False,
    tags=["inspiration", "daily_mental_service"]
) as dag:

    start_op = EmptyOperator(task_id="start")

    load_quote_op = PythonOperator(
        task_id="load_quote",
        python_callable=load_quote
    )

    load_image_op = PythonOperator(
        task_id="load_image",
        python_callable=load_image
    )

    send_to_teams_op = PythonOperator(
        task_id="send_to_teams",
        python_callable=send_to_teams
    )

    finish_op = EmptyOperator(task_id="finish")

    start_op >> [load_quote_op, load_image_op] >> send_to_teams_op >> finish_op
