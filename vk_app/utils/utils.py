import logging
import os
import threading
from datetime import datetime
from typing import Callable
from urllib.request import urlopen

__all__ = ['make_periodic', 'get_year_month_date', 'download', 'find_file', 'check_dir', 'get_valid_dirs']


def make_periodic(delay: int) -> Callable[[Callable], Callable]:
    """Decorator with parameter for making functions periodically launched
    :param delay: period in which function should be called, in seconds
    :return: periodic function
    """

    def launch_periodically(function: Callable) -> Callable:
        def launched_periodically(*args, **kwargs):
            timer = threading.Timer(delay, function, args=args, kwargs=kwargs)
            try:
                timer.start()
            except RuntimeError:
                timer.cancel()
                launched_periodically(*args, **kwargs)

        return launched_periodically

    return launch_periodically


@make_periodic(23)
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


def get_year_month_date(date_time: datetime, sep='.') -> str:
    year_month_date = date_time.strftime(sep.join(['%Y', '%m']))
    return year_month_date


def find_file(name: str, path: str):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None


def check_dir(path_dir: str, *subdirs):
    path = path_dir
    if not os.path.exists(path):
        os.mkdir(path)

    for ind, subdir in enumerate(subdirs):
        path = os.path.join(path, subdir)
        if not os.path.exists(path):
            os.mkdir(path)


def get_valid_dirs(*dirs) -> list:
    valid_dirs = filter(None, dirs)
    valid_dirs = list(valid_dirs)
    return valid_dirs
