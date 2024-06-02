import pymsteams
import logging

logger = logging.getLogger("ContentCreationLogger")


class MessageSender:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_to_teams(self, content):
        try:
            teams_message = pymsteams.connectorcard(self.webhook_url)
            teams_message.text(content)
            teams_message.send()
            logger.info("Content is succesfully sent to Microsoft Teams")
        except Exception as e:
            logger.error(f"Error sending content to Microsoft Teams: {e}")
