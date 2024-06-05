import logging
import os
from image_loader import UnsplashImageLoader
from quote_loader import QuotableQuoteLoader
from message_sender import TeamsMessageSender

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
        return f"Sent by {self.author_name}\n\nQuote: {quote}\n\n![Image]({image})"

    def run(self):
        content = self._create_content()
        if content:
            self.message_sender.send_to_teams(content)
        else:
            logger.error("Nothing to send to Microsoft Teams")
