import logging
import os

from image_loader import UnsplashImageLoader
from message_sender import TeamsMessageSender
from quote_loader import QuotableQuoteLoader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ContentCreationLogger")

AUTHOR_NAME = os.getenv("AUTHOR_NAME")


class ContentCreator:
    def __init__(self):
        self.quote_loader = QuotableQuoteLoader()
        self.image_loader = UnsplashImageLoader()
        self.message_sender = TeamsMessageSender()
        self.author_name = AUTHOR_NAME

    def _create_content(self):
        quote = self.quote_loader.get_quote()
        image = self.image_loader.get_image()
        if not (quote and image):
            logger.error("Failed to create content")
            return None

        logger.info("Content is created")
        return {
            "author": self.author_name,
            "quote": quote,
            "image_url": image
        }

    def run(self):
        content_data = self._create_content()
        if content_data:
            self.message_sender.send_to_teams(content_data)
        else:
            logger.error("Nothing to send to Microsoft Teams")
