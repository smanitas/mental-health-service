import logging
import os
import requests

logger = logging.getLogger("ContentCreationLogger")

IMAGE_API_URL = os.getenv("IMAGE_API_URL")


class UnsplashImageLoader:
    def __init__(self):
        self.api_url = IMAGE_API_URL

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
