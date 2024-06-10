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

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ContentCreationLogger")


def load_quote(ti):
    """Task to load a quote"""
    api_url = Variable.get("QUOTE_API_URL")
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        quote_data = response.json()
        quote = quote_data.get("content")
        author = quote_data.get("author")
        if quote and author:
            logger.info("Quote is successfully loaded")
            ti.xcom_push(key="quote", value=f"{quote} — {author}")
        else:
            logger.error("Failed to load quote")
            raise ValueError("Failed to load quote")
    except requests.exceptions.RequestException as e:
        logger.exception(f"Error loading quote: {e}")
        raise


def load_image(ti):
    """Task to load an image"""
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
            logger.info("Image URL is successfully loaded")
            ti.xcom_push(key="image_url", value=image_url)
        else:
            logger.error("Failed to load image URL")
            raise ValueError("Failed to load image URL")
    except requests.exceptions.RequestException as e:
        logger.exception("Error loading image")
        raise


def send_to_teams(**kwargs):
    """Task to send content to Microsoft Teams."""
    teams_conn = BaseHook.get_connection("TEAMS_WEBHOOK")
    webhook_url = teams_conn.host

    ti = kwargs["ti"]
    quote = ti.xcom_pull(task_ids="load_quote", key="quote")
    image_url = ti.xcom_pull(task_ids="load_image", key="image_url")
    author_name = Variable.get("AUTHOR_NAME")
    logger.debug(f"Using AUTHOR_NAME: {author_name}")

    if not quote or not image_url:
        logger.error("Missing quote or image URL")
        raise ValueError("Missing quote or image URL")

    content = (
        f"Sent by {author_name}\n\n"
        f"Quote: {quote}\n\n"
        f"![Image]({image_url})"
    )

    try:
        teams_message = pymsteams.connectorcard(webhook_url)
        teams_message.text(content)
        teams_message.send()
        logger.info("Content is successfully sent to Teams")
    except pymsteams.TeamsWebhookException as e:
        logger.exception(f"Failed to send content to Teams due to webhook error: {e}")
        raise
    except requests.RequestException as e:
        logger.exception(f"Failed to send content to Teams due to network connectivity issue: {e}")
        raise
    except Exception as e:
        logger.exception(f"An unexpected error occurred while sending content to Teams: {e}")
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
        python_callable=load_quote,
        provide_context=True,
    )

    load_image_op = PythonOperator(
        task_id="load_image",
        python_callable=load_image,
        provide_context=True,
    )

    send_to_teams_op = PythonOperator(
        task_id="send_to_teams",
        python_callable=send_to_teams,
        provide_context=True,
    )

    finish_op = EmptyOperator(task_id="finish")

    start_op >> [load_quote_op, load_image_op] >> send_to_teams_op >> finish_op
