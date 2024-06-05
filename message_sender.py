import logging
import os
import pymsteams
import requests

logger = logging.getLogger("ContentCreationLogger")

WEBHOOK_URL = os.getenv("WEBHOOK_URL")


class TeamsMessageSender:
    def __init__(self):
        self.webhook_url = WEBHOOK_URL

    def send_to_teams(self, content_data):
        try:
            content = (
                f"Sent by {content_data['author']}\n\n"
                f"Quote: {content_data['quote']}\n\n"
                f"![Image]({content_data['image_url']})"
            )
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
