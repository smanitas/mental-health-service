import logging
import os
import requests

logger = logging.getLogger("ContentCreationLogger")

UNSPLASH_TOKEN = os.getenv("UNSPLASH_TOKEN")


class UnsplashImageLoader:
    def __init__(self):
        self.api_url = (
            f"https://api.unsplash.com/photos/random"
            f"?query=nature"
            f"&orientation=landscape"
            f"&client_id={UNSPLASH_TOKEN}"
        )

    def get_image(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            image_url = response.json()['urls']['small']
            if image_url:
                logger.info("Image URL is successfully loaded")
                return image_url
            else:
                logger.error("Failed to load image URL")
                return None
        except requests.exceptions.RequestException as e:
            logger.exception("Error loading image")
            return None
