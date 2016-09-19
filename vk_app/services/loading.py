import logging
import os
from urllib.request import urlopen

from vk_app.utils import CallDelayer

__MINIMAL_INTERVAL_BETWEEN_REQUESTS_IN_SECONDS = 0.33


@CallDelayer.make_delayed(__MINIMAL_INTERVAL_BETWEEN_REQUESTS_IN_SECONDS)
def download(url: str, save_path: str):
    if not os.path.exists(save_path) and url:
        try:
            response = urlopen(url)
            if response.status == 200:
                with open(save_path, 'wb') as out:
                    image_content = response.read()
                    out.write(image_content)
        except (ValueError, OSError):
            error_description = "Can't download to {} from {}".format(save_path, url)
            logging.exception(error_description)
