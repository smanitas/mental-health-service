import requests
import logging

logger = logging.getLogger("ContentCreationLogger")


class QuoteLoader:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_quote(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            quote_data = response.json()[0]
            quote = quote_data.get('q')
            author = quote_data.get('a')
            if quote and author:
                logger.info("Quote is successfully loaded")
                return f"{quote} — {author}"
            else:
                logger.error("Failed to load quote")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error loading quote: {e}")
            return None
