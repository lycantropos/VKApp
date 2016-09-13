import os
import shutil

from vk_app.utils import find_file


class VKObject:
    def synchronize(self, path):
        file_name = self.get_file_name()
        old_file_path = find_file(file_name, path)
        if old_file_path:
            file_dir = self.get_file_dir(path)
            file_path = os.path.join(file_dir, file_name)
            shutil.move(old_file_path, file_path)
        else:
            self.download(path)

    def download(self, save_path: str):
        """Must be overridden by inheritors"""

    def get_file_dir(self, path: str) -> str:
        """Must be overridden by inheritors"""

    def get_file_name(self) -> str:
        """Must be overridden by inheritors"""

    @classmethod
    def name(cls) -> str:
        """
        For elements of attachments (such as VK photo, audio objects) should return their key in attachment object
        e.g. for VK photo object should return 'photo', for VK audio object should return 'audio' and etc.
        """

    @classmethod
    def info_fields(cls) -> list:
        """
        Should return list of VK object's fields names which should be updated in database
        if its row already exists
        """

    @classmethod
    def get_vk_objects_from_raw(cls, raw_vk_objects: list) -> list:
        vk_objects = list(
            cls.from_raw(raw_vk_object)
            for raw_vk_object in raw_vk_objects
        )
        return vk_objects

    @classmethod
    def from_raw(cls, raw_vk_object: dict):
        """Must be overridden by inheritors"""
