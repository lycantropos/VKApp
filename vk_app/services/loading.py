import logging
from urllib.request import urlopen


def download(url: str, save_path: str):
    logging.debug("Loading from {} to {}".format(url, save_path))
    try:
        response = urlopen(url)
        if response.status == 200:
            with open(save_path, 'wb') as out:
                file_content = response.read()
                out.write(file_content)
        return
    except OSError:
        logging.exception('Can\'t download from {} to {}. Skipping.'.format(url, save_path))
