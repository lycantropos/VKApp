import logging
from datetime import datetime
from time import sleep
from typing import List

from vk_app import MetaVKObject

__all__ = ['get_vk_objects_from_raw', 'get_raw_vk_objects_from_posts', 'download_vk_objects']


def get_vk_objects_from_raw(vk_object_cls: MetaVKObject, raw_vk_objects: List[dict]) -> List[MetaVKObject]:
    vk_objects = list(
        vk_object_cls.from_raw(raw_vk_object)
        for raw_vk_object in raw_vk_objects
    )
    return vk_objects


def get_raw_vk_objects_from_posts(vk_object_cls: MetaVKObject, posts: List[dict]) -> List[dict]:
    vk_object_name = vk_object_cls.name()
    raw_vk_objects = list(
        attachment[vk_object_name]
        for post in posts
        if 'attachments' in post
        for attachment in post['attachments']
        if vk_object_name in attachment
    )
    return raw_vk_objects


MINIMAL_INTERVAL_BETWEEN_REQUESTS_IN_SECONDS = 0.33


def download_vk_objects(vk_objects: List[MetaVKObject], save_path: str):
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
