import os
import shutil
from datetime import datetime, time, timedelta
from typing import List

from vk_app.services.loading import download
from vk_app.utils import find_file, check_dir, get_year_month_date, get_valid_dirs


class VKObject:
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
    def attachment_key(cls) -> str:
        """
        For elements of attachments (such as VK photo, audio objects) should return their key in attachment object
        e.g. for VK photo object should return 'photo', for VK audio object should return 'audio' and etc.
        """

    @classmethod
    def from_raw(cls, raw_vk_object: dict) -> type:
        """Must be overridden by inheritors"""


VK_ID_FORMAT = '{}_{}'


class VKPhoto(VKObject):
    def __init__(self, owner_id: int, photo_id: int, user_id: int, album: str, date_time: datetime, comment: str = '',
                 link: str = ''):
        # VK utility fields
        self.vk_id = VK_ID_FORMAT.format(owner_id, photo_id)
        self.owner_id = owner_id
        self.photo_id = photo_id
        self.user_id = user_id

        # info fields
        self.album = album
        self.comment = comment

        # technical info fields
        self.date_time = date_time
        self.link = link

    def __repr__(self):
        return "<Photo(album='{}', link='{}', date_time='{}')>".format(
            self.album, self.link, self.date_time
        )

    def __str__(self):
        return "Photo from '{}' album".format(self.album)

    @classmethod
    def attachment_key(cls) -> str:
        return 'photo'

    def download(self, path: str):
        image_subdirs = self.get_file_subdirs()
        check_dir(path, *image_subdirs)

        image_dir = os.path.join(path, *image_subdirs)
        image_name = self.get_file_name()
        image_path = os.path.join(image_dir, image_name)

        download(self.link, image_path)

    def get_file_subdirs(self) -> list:
        year_month_date = get_year_month_date(self.date_time)
        image_subdirs = get_valid_dirs(self.album, year_month_date)
        return image_subdirs

    def get_file_name(self) -> str:
        image_name = self.link.split('/')[-1]
        return image_name

    def get_image_content(self, images_path: str, marked=True) -> bytearray:
        image_path = self.get_file_path(images_path)
        if marked:
            image_path = image_path.replace('.jpg', '.png')

        with open(image_path, 'rb') as marked_image:
            image_content = marked_image.read()

        return image_content

    @classmethod
    def from_raw(cls, raw_photo: dict) -> VKObject:
        return cls(
            int(raw_photo['owner_id']),
            int(raw_photo['id']),
            int(raw_photo.get('user_id', 0)),
            raw_photo['album'],
            raw_photo['text'],
            datetime.fromtimestamp(raw_photo['date']),
            cls.get_link(raw_photo)
        )

    @staticmethod
    def get_link(raw_photo: dict) -> str:
        photo_link_key_prefix = 'photo_'

        photo_link_keys = list(
            raw_photo_key
            for raw_photo_key in raw_photo
            if photo_link_key_prefix in raw_photo_key
        )
        photo_link_keys.sort(key=lambda x: int(x.replace(photo_link_key_prefix, '')))

        highest_res_link_key = photo_link_keys[-1]
        highest_res_link = raw_photo[highest_res_link_key]

        return highest_res_link


MAX_FILE_NAME_LEN = os.pathconf(os.getcwd(), 'PC_NAME_MAX')


class VKAudio(VKObject):
    FILE_NAME_FORMAT = "{artist} - {title}"
    FILE_EXTENSION = ".mp3"

    def __init__(self, owner_id: int, audio_id: int, artist: str, title: str, duration: time, date_time: datetime,
                 genre_id: int = 0, lyrics_id: int = 0, link: str = ''):
        # VK utility fields
        self.vk_id = VK_ID_FORMAT.format(owner_id, audio_id)
        self.owner_id = owner_id
        self.audio_id = audio_id

        # info fields
        self.artist = artist
        self.title = title
        self.genre_id = genre_id
        self.lyrics_id = lyrics_id

        # technical info fields
        self.duration = duration
        self.date_time = date_time
        self.link = link

    def __repr__(self):
        return "<Audio(artist='{}', title='{}', duration='{}')>".format(
            self.artist, self.title, self.duration
        )

    def __str__(self):
        return "Audio called '{}'".format(
            VKAudio.FILE_NAME_FORMAT.format(**self.__dict__)
        )

    @classmethod
    def attachment_key(cls):
        return 'audio'

    def download(self, path: str):
        audio_file_subdirs = self.get_file_subdirs()
        check_dir(path, *audio_file_subdirs)

        audio_file_dir = os.path.join(path, *audio_file_subdirs)
        audio_file_name = self.get_file_name()
        audio_file_path = os.path.join(audio_file_dir, audio_file_name)

        download(self.link, audio_file_path)

    def get_file_subdirs(self) -> str:
        audio_file_subdirs = [self.artist]
        return audio_file_subdirs

    def get_file_name(self) -> str:
        file_name = VKAudio.FILE_NAME_FORMAT.format(
            **self.__dict__
        )[:MAX_FILE_NAME_LEN - len(VKAudio.FILE_EXTENSION)].replace(os.sep, ' ') + VKAudio.FILE_EXTENSION
        return file_name

    @classmethod
    def from_raw(cls, raw_vk_object: dict) -> VKObject:
        return cls(owner_id=int(raw_vk_object['owner_id']), audio_id=int(raw_vk_object['id']),
                   artist=raw_vk_object['artist'].strip(), title=raw_vk_object['title'].strip(),
                   duration=(
                       datetime.min + timedelta(
                           seconds=int(raw_vk_object['duration'])
                       )
                   ).time(),
                   date_time=datetime.fromtimestamp(raw_vk_object['date']),
                   genre_id=int(raw_vk_object.pop('genre_id', 0)),
                   lyrics_id=int(raw_vk_object.pop('lyrics_id', 0)),
                   link=raw_vk_object['url'] or None)
