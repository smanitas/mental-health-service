from image_loader import ImageLoader
from quote_loader import QuoteLoader
from message_sender import MessageSender
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ContentCreationLogger")


class ContentCreator:
    def __init__(self, quote_api_url, image_api_url, webhook_url, author_name):
        self.quote_loader = QuoteLoader(quote_api_url)
        self.image_loader = ImageLoader(image_api_url)
        self.message_sender = MessageSender(webhook_url)
        self.author_name = author_name

    def create_content(self):
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
        content = self.create_content()
        if content:
            self.message_sender.send_to_teams(content)
        else:
            logger.error("Nothing to send to Microsoft Teams")
