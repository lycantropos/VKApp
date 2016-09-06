import logging
from datetime import datetime
from time import sleep

MINIMAL_INTERVAL_BETWEEN_REQUESTS_IN_SECONDS = 0.33


def download_vk_objects(vk_objects: list, save_path: str):
    last_download_time = datetime.utcnow()
    for vk_object in vk_objects:
        try:
            # we can send request to VK servers only 3 times a second
            time_elapsed_since_last_download = (datetime.utcnow() - last_download_time).total_seconds()
            if time_elapsed_since_last_download < MINIMAL_INTERVAL_BETWEEN_REQUESTS_IN_SECONDS:
                sleep(MINIMAL_INTERVAL_BETWEEN_REQUESTS_IN_SECONDS - time_elapsed_since_last_download)
            last_download_time = datetime.utcnow()

            vk_object.download(save_path)
        except OSError as e:
            # e.g. raises when there is no vk_object found by link on the server anymore
            logging.info(vk_object)
            logging.exception(e)


class VKObject:
    def download(self):
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
        return cls.__class__.__name__.lower()

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
