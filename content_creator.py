import logging
import os
from image_loader import ImageLoader
from quote_loader import QuoteLoader
from message_sender import MessageSender

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ContentCreationLogger")

QUOTE_API_URL = os.getenv("QUOTE_API_URL")
IMAGE_API_URL = os.getenv("IMAGE_API_URL")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
AUTHOR_NAME = os.getenv("AUTHOR_NAME")


class ContentCreator:
    def __init__(self):
        self.quote_loader = QuoteLoader(QUOTE_API_URL)
        self.image_loader = ImageLoader(IMAGE_API_URL)
        self.message_sender = MessageSender(WEBHOOK_URL)
        self.author_name = AUTHOR_NAME

    def _create_content(self):
        quote = self.quote_loader.get_quote()
        image = self.image_loader.get_image()
        if quote and image:
            content = f"Sent by {self.author_name}\n\nQuote: {quote}\n\n![Image]({image})"
            logger.info("Content is created")
            return content
        else:
            logger.error("Failed to create content")
            return None

    def run(self):
        content = self._create_content()
        if content:
            self.message_sender.send_to_teams(content)
        else:
            logger.error("Nothing to send to Microsoft Teams")
