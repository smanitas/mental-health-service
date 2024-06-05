import logging
import requests

logger = logging.getLogger("ContentCreationLogger")


class QuotableQuoteLoader:
    def __init__(self):
        self.api_url = "https://api.quotable.io/random?tags=Happiness"

    def get_quote(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            quote_data = response.json()
            quote = quote_data.get("content")
            author = quote_data.get("author")
            if quote and author:
                logger.info("Quote is successfully loaded")
                return f"{quote} — {author}"
            else:
                logger.error("Failed to load quote")
                return None
        except requests.exceptions.RequestException as e:
            logger.exception(f"Error loading quote: {e}")
            return None
