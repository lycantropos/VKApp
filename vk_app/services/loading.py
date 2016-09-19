import logging
import os
from urllib.request import urlopen

from vk_app.utils import CallDelayer

__MINIMAL_INTERVAL_BETWEEN_REQUESTS_IN_SECONDS = 0.35


@CallDelayer.make_delayed(__MINIMAL_INTERVAL_BETWEEN_REQUESTS_IN_SECONDS)
def download(url: str, save_path: str):
    logging.debug("Loading to {} from {}".format(save_path, url))
    if not os.path.exists(save_path) and url:
        try:
            response = urlopen(url)
            if response.status == 200:
                with open(save_path, 'wb') as out:
                    image_content = response.read()
                    out.write(image_content)
        except OSError:
            logging.exception("Can't download to {} from {}. Retrying...".format(save_path, url))
            download(url, save_path)
