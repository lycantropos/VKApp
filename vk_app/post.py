import logging
from datetime import datetime
from typing import Dict, List, Any

from vk_app.attachables import VKObject, VKAttachable
from vk_app.utils import get_all_subclasses

ATTACHMENTS_KEY_VK_ATTACHABLE = dict(
    (inheritor.key(), inheritor)
    for inheritor in get_all_subclasses(VKAttachable)
    if inheritor.key() is not None
)


class VKPost(VKObject):
    """
    Implements working with VK wall posts

    more info about `Post` objects at https://vk.com/dev/post
    """

    def __init__(self, owner_id: int, object_id: int, from_id: int, created_by: int,
                 text: str, attachments: List[Dict[str, VKAttachable]], date_time: datetime,
                 likes_count: int, reposts_count: int, comments_count: int):
        super().__init__(owner_id, object_id)

        # VK utility fields
        self.from_id = from_id
        self.created_by = created_by

        # info fields
        self.text = text
        self.attachments = attachments

        # technical info fields
        self.date_time = date_time
        self.likes_count = likes_count
        self.reposts_count = reposts_count
        self.comments_count = comments_count

    @classmethod
    def from_raw(cls, raw_post: dict) -> VKObject:
        return cls(
            owner_id=int(raw_post['owner_id']),
            object_id=int(raw_post['id']),
            from_id=int(raw_post.get('from_id', 0)),
            created_by=int(raw_post.get('created_by', 0)),
            text=raw_post.get('text', None),
            attachments=cls.attachments_from_raw(raw_post.get('attachments', [])),
            date_time=datetime.fromtimestamp(int(raw_post['date'])),
            likes_count=int(raw_post['likes']['count']),
            reposts_count=int(raw_post['reposts']['count']),
            comments_count=int(raw_post['comments']['count'])
        )

    @staticmethod
    def attachments_from_raw(raw_attachments: List[Dict[str, Any]], required_keys: List[str] = None,
                             forbidden_keys: List[str] = None) -> List[Dict[str, VKAttachable]]:
        if not required_keys or not forbidden_keys or \
                not any(required_key in forbidden_keys for required_key in required_keys):
            attachments = list()
            for raw_attachment in raw_attachments:
                key = raw_attachment['type']
                content = raw_attachment[key]
                if (not required_keys or key in required_keys) and \
                        (not forbidden_keys or key not in forbidden_keys):
                    try:
                        attachments.append(
                            {key: ATTACHMENTS_KEY_VK_ATTACHABLE[key].from_raw(content)}
                        )
                    except KeyError:
                        logging.warning('No support found for attachment type: "{}"'.format(key))
            return attachments
        else:
            raise ValueError('Invalid data format: required and forbidden keys lists should have empty intersection')
