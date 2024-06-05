import logging
import os
import pymsteams
import requests

logger = logging.getLogger("ContentCreationLogger")

WEBHOOK_URL = os.getenv("WEBHOOK_URL")


class TeamsMessageSender:
    def __init__(self):
        self.webhook_url = WEBHOOK_URL

    def send_to_teams(self, content):
        try:
            teams_message = pymsteams.connectorcard(self.webhook_url)
            teams_message.text(content)
            teams_message.send()
            logger.info("Content is succesfully sent to Teams")
        except pymsteams.TeamsWebhookException as e:
            logger.exception(f"Failed to send content to Teams due to webhook error: {e}")
        except requests.RequestException as e:
            logger.exception(f"Failed to send content to Teams due to network connectivity issue: {e}")
        except Exception as e:
            logger.exception(f"An unexpected error while sending content to Teams: {e}")
