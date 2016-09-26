from typing import List

from vk_app.models import VKObject

__all__ = ['get_raw_vk_objects_from_posts']


def get_raw_vk_objects_from_posts(vk_object_cls: VKObject, posts: List[dict]) -> List[dict]:
    vk_object_name = vk_object_cls.attachment_key()
    raw_vk_objects = list(
        attachment[vk_object_name]
        for post in posts
        if 'attachments' in post
        for attachment in post['attachments']
        if vk_object_name in attachment
    )
    return raw_vk_objects
