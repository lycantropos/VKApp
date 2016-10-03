from datetime import datetime
from typing import Dict, List

from models.abstract import VKAttachment, VKObject

ATTACHMENTS_KEY_VK_OBJECT = dict(
    (inheritor.key(), inheritor)
    for inheritor in VKAttachment.__subclasses__()
)


class VKPost(VKObject):
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
    def get_attachments_from_raw(raw_attachments: List[Dict[str, dict]], attachment_key: str = None):
        attachments = dict()
        for raw_attachment in raw_attachments:
            for key, content in raw_attachment.items():
                if (not attachment_key or key == attachment_key) and key in ATTACHMENTS_KEY_VK_OBJECT:
                    attachments.setdefault(key, []).append(ATTACHMENTS_KEY_VK_OBJECT[key].from_raw(content))
        return attachments
