import logging
from datetime import datetime
from typing import Dict, List

from vk_app.models.abstract import VKAttachment, VKObject
from vk_app.utils import get_all_subclasses

ATTACHMENTS_KEY_VK_OBJECT = dict(
    (inheritor.key(), inheritor)
    for inheritor in get_all_subclasses(VKAttachment)
    if inheritor.key()
)


class VKPost(VKObject):
    """
    Implements working with VK wall posts

    more info about `Post` objects at https://vk.com/dev/post
    """
    def __init__(self, owner_id: int, object_id: int, from_id: int, created_by: int,
                 comment: str, attachments: Dict[str, List[VKAttachment]], date_time: datetime,
                 likes_count: int, reposts_count: int, comments_count: int):
        super().__init__(owner_id, object_id)

        # VK utility fields
        self.from_id = from_id
        self.created_by = created_by

        # info fields
        self.comment = comment
        self.attachments = attachments

        # technical info fields
        self.date_time = date_time
        self.likes_count = likes_count
        self.reposts_count = reposts_count
        self.comments_count = comments_count

    def __eq__(self, other: VKObject):
        if type(self) is type(other):
            return self.vk_id == other.vk_id and \
                   self.date_time == other.date_time and \
                   all(attachments_list == self.attachments[key] for key, attachments_list in other.attachments.items())
        else:
            return NotImplemented

    def __ne__(self, other: VKObject):
        return not self == other

    @classmethod
    def from_raw(cls, raw_post: dict) -> VKObject:
        return cls(
            owner_id=int(raw_post['owner_id']),
            object_id=int(raw_post['id']),
            from_id=int(raw_post.get('from_id', 0)),
            created_by=int(raw_post.get('created_by', 0)),
            comment=raw_post.get('text', None),
            attachments=VKPost.get_attachments_from_raw(raw_post.get('attachments', [])),
            date_time=datetime.fromtimestamp(int(raw_post['date'])),
            likes_count=int(raw_post['likes']['count']),
            reposts_count=int(raw_post['reposts']['count']),
            comments_count=int(raw_post['comments']['count'])
        )

    @staticmethod
    def get_attachments_from_raw(raw_attachments: List[Dict[str, dict]], required_keys: List[str] = None,
                                 forbidden_keys: List[str] = None):
        if not required_keys or not forbidden_keys or \
                not any(required_key in forbidden_keys for required_key in required_keys):
            attachments = dict()
            for raw_attachment in raw_attachments:
                key = raw_attachment['type']
                content = raw_attachment[key]
                if (not required_keys or key in required_keys) and \
                        (not forbidden_keys or key not in forbidden_keys):
                    if key in ATTACHMENTS_KEY_VK_OBJECT:
                        attachments.setdefault(key, []).append(ATTACHMENTS_KEY_VK_OBJECT[key].from_raw(content))
                    else:
                        logging.warning("No support found for attachment type: '{}'".format(key))
            return attachments
        else:
            raise ValueError("Invalid data format: required and forbidden keys lists should have empty intersection")
