from typing import List

from models import VKObject

__all__ = ['get_vk_objects_from_raw', 'get_raw_vk_objects_from_posts']


def get_vk_objects_from_raw(vk_object_cls: VKObject, raw_vk_objects: List[dict]) -> List[VKObject]:
    vk_objects = list(
        vk_object_cls.from_raw(raw_vk_object)
        for raw_vk_object in raw_vk_objects
    )
    return vk_objects


def get_raw_vk_objects_from_posts(vk_object_cls: VKObject, posts: List[dict]) -> List[dict]:
    vk_object_name = vk_object_cls.name()
    raw_vk_objects = list(
        attachment[vk_object_name]
        for post in posts
        if 'attachments' in post
        for attachment in post['attachments']
        if vk_object_name in attachment
    )
    return raw_vk_objects
