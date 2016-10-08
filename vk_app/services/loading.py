import logging
import os
from urllib.request import urlopen


def download(url: str, save_path: str):
    logging.debug("Loading from {} to {}".format(url, save_path))
    if not os.path.exists(save_path) and url:
        try:
            response = urlopen(url)
            if response.status == 200:
                with open(save_path, 'wb') as out:
                    file_content = response.read()
                    out.write(file_content)
        except OSError:
            logging.exception("Can't download from {} to {}. Retrying...".format(url, save_path))
            download(url, save_path)
