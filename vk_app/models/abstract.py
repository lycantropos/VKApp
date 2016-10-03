import os
import shutil
from datetime import datetime
from typing import List

from utils import find_file, check_dir

VK_ID_FORMAT = '{}_{}'


class VKObject:
    def __init__(self, owner_id: int, object_id: int):
        # VK utility fields
        self.vk_id = VK_ID_FORMAT.format(owner_id, object_id)
        self.owner_id = owner_id
        self.object_id = object_id

    def __eq__(self, other):
        if type(self) is type(other):
            return self.vk_id == other.vk_id
        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    @classmethod
    def from_raw(cls, raw_vk_object: dict) -> type:
        """Must be overridden by inheritors"""


class VKAttachment(VKObject):
    def __init__(self, owner_id: int, object_id: int, link: str):
        super().__init__(owner_id, object_id)

        # technical info fields
        self.link = link

    def __eq__(self, other):
        if type(self) is type(other):
            return self.vk_id == other.vk_id and \
                   self.link == other.link
        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    def synchronize(self, path: str, files_paths=None):
        file_name = self.get_file_name()
        if files_paths is not None:
            old_file_path = next((file_path for file_path in files_paths if file_name in file_path), None)
        else:
            old_file_path = find_file(file_name, path)
        if old_file_path is not None:
            file_subdirs = self.get_file_subdirs()
            check_dir(path, *file_subdirs)

            file_dir = os.path.join(path, *file_subdirs)
            file_path = os.path.join(file_dir, file_name)

            shutil.move(old_file_path, file_path)
        else:
            self.download(path)

    def download(self, path: str):
        """Must be overridden by inheritors"""

    def get_file_path(self, path: str) -> str:
        file_name = self.get_file_name()
        file_subdirs = self.get_file_subdirs()
        file_path = os.path.join(path, *file_subdirs, file_name)
        return file_path

    def get_file_subdirs(self) -> List[str]:
        """
        Should return list of subdirectories names for file to be located at

        Must be overridden by inheritors
        """

    def get_file_name(self) -> str:
        """Must be overridden by inheritors"""

    @classmethod
    def key(cls) -> str:
        """
        For elements of attachments (such as VK photo, audio objects) should return their key in attachment object
        e.g. for VK photo object should return 'photo', for VK audio object should return 'audio' and etc.
        """
