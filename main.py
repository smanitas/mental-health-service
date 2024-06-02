import os
from content_creator import ContentCreator

if __name__ == "__main__":
    QUOTE_API_URL = os.getenv("QUOTE_API_URL")
    IMAGE_API_URL = os.getenv("IMAGE_API_URL")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    AUTHOR_NAME = os.getenv("AUTHOR_NAME")

    content_creator = ContentCreator(QUOTE_API_URL, IMAGE_API_URL, WEBHOOK_URL, AUTHOR_NAME)
    content_creator.run()
