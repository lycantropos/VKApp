import logging
from datetime import datetime
from time import sleep

MINIMAL_INTERVAL_BETWEEN_REQUESTS_IN_SECONDS = 0.33


def download_vk_objects(vk_objects: list, save_path: str):
    last_download_time = datetime.utcnow()
    for ind, vk_object in enumerate(vk_objects):
        logging.info(vk_object)
        try:
            # we can send request to VK servers only 3 times a second
            time_elapsed_since_last_download = (datetime.utcnow() - last_download_time).total_seconds()
            if time_elapsed_since_last_download < MINIMAL_INTERVAL_BETWEEN_REQUESTS_IN_SECONDS:
                sleep(MINIMAL_INTERVAL_BETWEEN_REQUESTS_IN_SECONDS - time_elapsed_since_last_download)
            last_download_time = datetime.utcnow()

            vk_object.download(save_path)

            logging.info('{} {} of {} has been downloaded'.format(ordinal(ind), vk_object, len(vk_objects)))
        except OSError as e:
            # e.g. raises when there is no vk_object found by link on the server anymore
            logging.exception(e)


ORDINAL_RULES = {1: 'st', 2: 'nd', 3: 'rd'}
ORDINAL_RULES_EXCEPTIONS = {11, 12, 13}


def ordinal(n: int) -> str:
    suffix = ORDINAL_RULES[n % 10] if n % 10 in ORDINAL_RULES and n not in ORDINAL_RULES_EXCEPTIONS else 'th'
    return str(n) + suffix


class VKObject:
    def download(self, save_path: str):
        """Must be overridden by inheritors"""

    @classmethod
    def get_raw_from_posts(cls, posts: list) -> list:
        vk_object_name = cls.get_name()
        raw_vk_objects = list(
            attachment[vk_object_name]
            for post in posts
            if 'attachments' in post
            for attachment in post['attachments']
            if vk_object_name in attachment
        )
        return raw_vk_objects

    @classmethod
    def get_name(cls):
        """
        Written assuming that inheritor class called after specified VK object,
        e. g. Photo, Audio, Video
        """
        return cls.__name__.lower()

    @classmethod
    def get_vk_objects_from_raw(cls, raw_vk_objects: list) -> list:
        vk_objects = list(
            cls.from_raw(raw_vk_object)
            for raw_vk_object in raw_vk_objects
        )
        return vk_objects

    @classmethod
    def from_raw(cls, raw_vk_object: dict):
        """Must be overridden by inheritors"""
