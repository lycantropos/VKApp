from vk_app.utils import get_repr, obj_to_dict

VK_ID_FORMAT = '{owner_id}_{object_id}'


class VKObject:
    """
    Abstract class for working with VK data types

    more info about `Data types` at https://vk.com/dev/datatypes
    """

    def __init__(self, owner_id: int, object_id: int):
        # VK utility fields
        self.vk_id = VK_ID_FORMAT.format(owner_id=owner_id, object_id=object_id)
        self.owner_id = owner_id
        self.object_id = object_id

    def __eq__(self, other):
        if type(self) is type(other):
            return self.vk_id == other.vk_id
        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.vk_id)

    def __repr__(self):
        return get_repr(self)

    @classmethod
    def from_raw(cls, raw_vk_object: dict) -> type:
        """Must be overridden by inheritors"""

    def to_dict(self):
        return obj_to_dict(self)


class VKAttachable(VKObject):
    """
    Abstract class for working with VK media attachments in wall posts

    more info about `Media Attachments` at https://vk.com/dev/attachments_w
    """

    @classmethod
    def key(cls) -> str:
        """
        For elements of attachments (such as VK photo, audio objects) should return their key in attachment object
        e.g. for VK photo object should return 'photo', for VK audio object should return 'audio' and etc.
        """
