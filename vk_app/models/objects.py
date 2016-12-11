import logging
import os
import shutil
from typing import List, Dict, Any

from vk_app.services import download
from vk_app.utils import get_repr, obj_to_dict, find_file, check_dir

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

    def __eq__(self, other: 'VKObject'):
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
    def from_raw(cls, raw_vk_object: dict) -> 'VKObject':
        """Must be overridden by inheritors"""

    def to_dict(self) -> Dict[str, Any]:
        return obj_to_dict(self)


class VKAttachable(VKObject):
    """
    Abstract class for working with VK media attachments in wall posts and private messages

    attachment object are consist of type name and attachable (content)

    more info about `Media Attachments` at
    https://vk.com/dev/attachments_w
    https://vk.com/dev/attachments_m
    """

    @classmethod
    def key(cls) -> str:
        """
        Returns type of attachment object corresponding to given attachable
        (such as VK photo/audio objects)
        """


class VKFileAttachable(VKAttachable):
    """
    Abstract class for working with VK downloadable attachments like photos, audios and etc.

    more info about `Media Attachments` at https://vk.com/dev/attachments_w
    """

    def __init__(self, owner_id: int, object_id: int, link: str = None):
        super().__init__(owner_id, object_id)

        # technical info fields
        self.link = link

    def __ne__(self, other):
        return not self == other

    def synchronize(self, path: str, files_paths=None):
        file_name = self.get_file_name()
        if files_paths is not None:
            old_file_path = next((file_path
                                  for file_path in files_paths
                                  if file_name in file_path),
                                 None)
        else:
            old_file_path = find_file(file_name, path)
        if old_file_path is not None:
            file_subdirs = self.get_file_subdirs()
            check_dir(path, *file_subdirs, create=True)

            file_dir = os.path.join(path, *file_subdirs)
            file_path = os.path.join(file_dir, file_name)

            shutil.move(old_file_path, file_path)
        else:
            self.download(path)

    def download(self, path: str, **kwargs) -> str:
        """Downloads `VKFileAttachable` object into file system"""
        file_subdirs = self.get_file_subdirs()
        check_dir(path, *file_subdirs, create=True)

        file_dir = os.path.join(path, *file_subdirs)
        file_name = self.get_file_name()
        file_path = os.path.join(file_dir, file_name)

        if self.link and not os.path.exists(file_path):
            download(self.link, file_path)
        return file_path

    def get_file_content(self, path: str, **kwargs) -> bytearray:
        file_path = self.get_file_path(path, **kwargs)
        with open(file_path, 'rb') as file:
            file_content = file.read()

        return file_content

    def get_file_path(self, path: str, **kwargs) -> str:
        file_name = self.get_file_name(**kwargs)
        file_subdirs = self.get_file_subdirs()
        file_path = os.path.join(path, *file_subdirs, file_name)
        return file_path

    def get_file_subdirs(self) -> List[str]:
        """
        Returns list of subdirectories names for file to be located at
        """
        return []

    def get_file_name(self, **kwargs) -> str:
        """Must be overridden by inheritors"""

    def get_file_extension(self, **kwargs) -> str:
        """Must be overridden by inheritors"""

    @classmethod
    def getUploadServer_method(cls, dst_type: str) -> str:
        """
        Returns name of VK API method to get URL address of upload server with

        more info about VK API methods at https://vk.com/dev/methods

        :param dst_type: specific type of destination if supported.
        Ex. for class 'VKPhoto':
         dst_type='wall'
         to get method name for receiving image upload on community/user wall server URL
        """

    @classmethod
    def save_method(cls, dst_type: str) -> str:
        """
        Returns name of VK API method to save VK objects with

        more info about VK API methods at https://vk.com/dev/methods
        :param dst_type: specific type of destination if supported.
        Ex. for class 'VKPhoto':
         dst_type='wall'
         to get method name for image uploading on community/user wall
        """


class VKContainer(VKObject):
    """
    Abstract class for working with VK objects containers such as wall posts and private messages

    containers are objects with media attachments in them

    more info about `Containers` at
    https://vk.com/dev/post
    https://vk.com/dev/message
    """

    def __init__(self, owner_id: int, object_id: int,
                 attachments: List[Dict[str, VKAttachable]]):
        super().__init__(owner_id, object_id)

        # info fields
        self.attachments = attachments

    @classmethod
    def attachments_from_raw(cls, raw_attachments: List[Dict[str, Any]], required_keys: List[str] = None,
                             forbidden_keys: List[str] = None) -> List[Dict[str, VKAttachable]]:
        if forbidden_keys is not None and \
                        required_keys is not None and \
                any(required_key in forbidden_keys
                    for required_key in required_keys):
            err_message = 'Invalid data format: ' \
                          'required and forbidden keys lists ' \
                          'should have empty intersection.'
            raise ValueError(err_message)

        attachments = list()
        for raw_attachment in raw_attachments:
            type_name = raw_attachment['type']
            content = raw_attachment[type_name]
            if (not required_keys or type_name in required_keys) and \
                    (not forbidden_keys or type_name not in forbidden_keys):
                try:
                    attachments.append(
                        {type_name: cls.get_attachable_cls(type_name).from_raw(content)}
                    )
                except KeyError:
                    logging.warning('No support found for attachment type: "{}"'.format(type_name))
        return attachments

    @classmethod
    def get_attachable_cls(cls, type_name: str) -> VKAttachable:
        """Returns VKAttachable class by VK attachment type key"""
