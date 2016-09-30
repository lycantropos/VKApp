from typing import List

from vk_app.models import VKAttachment

__all__ = ['get_raw_vk_attachments_from_posts']


def get_raw_vk_attachments_from_posts(vk_attachment_cls: VKAttachment, posts: List[dict]) -> List[dict]:
    vk_attachment_name = vk_attachment_cls.key()
    raw_vk_objects = list(
        attachment[vk_attachment_name]
        for post in posts
        for attachment in post.get('attachments', [])
        if vk_attachment_name in attachment
    )
    return raw_vk_objects
