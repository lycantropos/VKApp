import logging
import os
import threading
from datetime import datetime
from time import sleep
from urllib.request import urlopen


def make_periodic(delay: int):
    """Decorator with parameter for making functions periodically launched
    :param delay: period in which function should be called, in seconds
    :return: periodic function
    """

    def launch_periodically(function):
        def launched_periodically(*args, **kwargs):
            timer = threading.Timer(delay, function, args=args, kwargs=kwargs)
            try:
                timer.start()
            except RuntimeError:
                timer.cancel()
                launched_periodically(*args, **kwargs)

        return launched_periodically

    return launch_periodically


def get_raw_vk_objects_from_posts(vk_object_class, posts: list) -> list:
    vk_object_name = vk_object_class.name()
    raw_vk_objects = list(
        attachment[vk_object_name]
        for post in posts
        if 'attachments' in post
        for attachment in post['attachments']
        if vk_object_name in attachment
    )
    return raw_vk_objects


MINIMAL_INTERVAL_BETWEEN_REQUESTS_IN_SECONDS = 0.33


def download_vk_objects(vk_objects: list, save_path: str):
    last_download_time = datetime.utcnow()
    for ind, vk_object in enumerate(vk_objects):
        try:
            # we can send request to VK servers only 3 times a second
            time_elapsed_since_last_download = (datetime.utcnow() - last_download_time).total_seconds()
            if time_elapsed_since_last_download < MINIMAL_INTERVAL_BETWEEN_REQUESTS_IN_SECONDS:
                sleep(MINIMAL_INTERVAL_BETWEEN_REQUESTS_IN_SECONDS - time_elapsed_since_last_download)
            last_download_time = datetime.utcnow()

            vk_object.download(save_path)

            logging.info("{} of {}: {} has been downloaded".format(ind + 1, len(vk_objects), vk_object))
        except OSError as e:
            # e.g. raises when there is no vk_object found by link on the server anymore
            logging.exception(e)


def download(link: str, save_path: str):
    if not os.path.exists(save_path):
        try:
            response = urlopen(link)
            if response.status == 200:
                with open(save_path, 'wb') as out:
                    image_content = response.read()
                    out.write(image_content)
        except ValueError as e:
            logging.exception(e)


def get_year_month_date(date_time: datetime, sep='.') -> str:
    year_month_date = date_time.strftime(sep.join(['%Y', '%m']))
    return year_month_date


def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None


def check_dir(folder_path: str, *subfolders):
    full_path = os.path.join(folder_path, *subfolders)
    if not os.path.exists(full_path):
        os.mkdir(full_path)


def get_valid_folders(*folders) -> list:
    valid_folders = filter(None, folders)
    valid_folders = list(valid_folders)
    return valid_folders


__all__ = [make_periodic, get_year_month_date, get_raw_vk_objects_from_posts,
           download_vk_objects, download, find_file, check_dir, get_valid_folders]
