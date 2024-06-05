import logging
import pymsteams
import requests

logger = logging.getLogger("ContentCreationLogger")


class MessageSender:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_to_teams(self, content):
        try:
            teams_message = pymsteams.connectorcard(self.webhook_url)
            teams_message.text(content)
            teams_message.send()
            logger.info(content)
            logger.info("Content is succesfully sent to Teams")
        except pymsteams.TeamsWebhookException as e:
            logger.error(f"Failed to send content to Teams due to webhook error: {e}")
        except requests.RequestException as e:
            logger.error(f"Failed to send content to Teams due to network connectivity issue: {e}")
        except Exception as e:
            logger.error(f"An unexpected error while sending content to Teams: {e}")
