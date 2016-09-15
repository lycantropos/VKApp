import logging
import os
from urllib.request import urlopen

from utils import CallDelayer

__MINIMAL_INTERVAL_BETWEEN_REQUESTS_IN_SECONDS = 0.33


@CallDelayer.make_delayed(__MINIMAL_INTERVAL_BETWEEN_REQUESTS_IN_SECONDS)
def download(link: str, save_path: str):
    if not os.path.exists(save_path):
        try:
            response = urlopen(link)
            if response.status == 200:
                with open(save_path, 'wb') as out:
                    image_content = response.read()
                    out.write(image_content)
        except (ValueError, OSError):
            logging.exception(save_path)
