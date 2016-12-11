import datetime
from typing import Dict, List

from vk_app.models.objects import VKAttachable, VKContainer, VKFileAttachable
from vk_app.utils import get_all_subclasses

__all__ = ['VKPost', 'VKMessage']


class VKPost(VKContainer):
    """
    Implements working with VK wall posts

    more info about `Post` objects at https://vk.com/dev/post
    """
    VK_ATTACHABLE_BY_KEY = dict(
        (inheritor.key(), inheritor)
        for inheritor in get_all_subclasses(VKAttachable)
        if inheritor.key() is not None
    )

    def __init__(self, owner_id: int, object_id: int, from_id: int, created_by: int,
                 text: str, attachments: List[Dict[str, VKAttachable]],
                 date_time: datetime.datetime,
                 likes_count: int, reposts_count: int, comments_count: int):
        super().__init__(owner_id, object_id, attachments)

        # VK utility fields
        self.from_id = from_id
        self.created_by = created_by

        # info fields
        self.text = text

        # technical info fields
        self.date_time = date_time
        self.likes_count = likes_count
        self.reposts_count = reposts_count
        self.comments_count = comments_count

    @classmethod
    def from_raw(cls, raw_post: dict) -> 'VKPost':
        return cls(
            owner_id=int(raw_post['owner_id']),
            object_id=int(raw_post['id']),
            from_id=int(raw_post.get('from_id', 0)),
            created_by=int(raw_post.get('created_by', 0)),
            text=raw_post.get('text', None),
            attachments=cls.attachments_from_raw(raw_post.get('attachments', [])),
            date_time=datetime.datetime.utcfromtimestamp(int(raw_post['date'])),
            likes_count=int(raw_post['likes']['count']),
            reposts_count=int(raw_post['reposts']['count']),
            comments_count=int(raw_post['comments']['count'])
        )

    @classmethod
    def get_attachable_cls(cls, type_name: str) -> VKAttachable:
        return cls.VK_ATTACHABLE_BY_KEY[type_name]


class VKMessage(VKContainer):
    """
    Implements working with VK private messages

    more info about `Message` objects at https://vk.com/dev/message
    """
    VK_ATTACHABLE_BY_KEY = dict(
        (inheritor.key(), inheritor)
        for inheritor in get_all_subclasses(VKFileAttachable)
        if inheritor.key() is not None
    )

    def __init__(self, owner_id: int, object_id: int,
                 title: str, body: str,
                 attachments: List[Dict[str, VKAttachable]],
                 date_time: datetime.datetime,
                 sent: bool, read: bool, deleted: bool, emojied: bool,
                 forwarded_messages=None):
        super().__init__(owner_id, object_id, attachments)

        # info fields
        self.title = title
        self.body = body
        self.forwarded_messages = forwarded_messages

        # technical info fields
        self.date_time = date_time
        self.sent = sent
        self.read = read
        self.deleted = deleted
        self.emojied = emojied

    @classmethod
    def from_raw(cls, raw_message: dict) -> 'VKMessage':
        # forwarded message only has `user_id`, `date`, `body` and/or `attachments`
        return cls(
            # for an incoming message, the user ID of the author
            # for an outgoing message, the user ID of the receiver
            owner_id=raw_message['user_id'],
            object_id=raw_message.get('id', 0),
            title=raw_message.get('title'),
            body=raw_message['body'],
            attachments=cls.attachments_from_raw(raw_message.get('attachments', [])),
            date_time=datetime.datetime.utcfromtimestamp(raw_message['date']),
            sent=raw_message.get('out', 0) == 1,
            read=raw_message.get('read_state', 0) == 1,
            deleted=raw_message.get('deleted', 0) == 1,
            emojied=raw_message.get('emoji', 0) == 1,
            forwarded_messages=list(map(cls.from_raw, raw_message.get('fwd_messages', [])))
        )

    @classmethod
    def get_attachable_cls(cls, type_name: str) -> VKAttachable:
        return cls.VK_ATTACHABLE_BY_KEY[type_name]
