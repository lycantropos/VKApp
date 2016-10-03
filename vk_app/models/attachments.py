import os
import re
from datetime import datetime, time, timedelta
from typing import List

from models.abstract import VKAttachment, VKObject
from services.loading import download
from utils import check_dir, get_year_month_date, get_valid_dirs


class VKPhoto(VKAttachment):
    def __init__(self, owner_id: int, object_id: int, user_id: int, album: str, date_time: datetime, comment: str = '',
                 link: str = ''):
        super().__init__(owner_id, object_id, link)

        # VK utility fields
        self.user_id = user_id

        # info fields
        self.album = album
        self.comment = comment

        # technical info fields
        self.date_time = date_time

    def __repr__(self):
        return "<Photo(album='{}', link='{}', date_time='{}')>".format(
            self.album, self.link, self.date_time
        )

    def __str__(self):
        return "Photo from '{}' album".format(self.album)

    @classmethod
    def key(cls) -> str:
        return 'photo'

    def download(self, path: str):
        image_subdirs = self.get_file_subdirs()
        check_dir(path, *image_subdirs)

        image_dir = os.path.join(path, *image_subdirs)
        image_name = self.get_file_name()
        image_path = os.path.join(image_dir, image_name)

        download(self.link, image_path)

    def get_file_subdirs(self) -> List[str]:
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
            owner_id=int(raw_photo['owner_id']),
            object_id=int(raw_photo['id']),
            user_id=int(raw_photo.get('user_id', 0)),
            album=SPECIAL_ALBUMS_IDS_TITLES.get(int(raw_photo['album_id']), None),
            comment=raw_photo['text'],
            date_time=datetime.fromtimestamp(int(raw_photo['date'])),
            link=cls.get_link(raw_photo)
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


SPECIAL_ALBUMS_IDS_TITLES = {
    -6: 'profile',
    -7: 'wall',
    -15: 'saved'
}
MAX_FILE_NAME_LEN = os.pathconf(os.getcwd(), 'PC_NAME_MAX')


class VKAudio(VKAttachment):
    FILE_NAME_FORMAT = "{artist} - {title}"
    FILE_EXTENSION = ".mp3"

    def __init__(self, owner_id: int, object_id: int, artist: str, title: str, duration: time, date_time: datetime,
                 genre_id: int = 0, lyrics_id: int = 0, link: str = ''):
        super().__init__(owner_id, object_id, link)

        # info fields
        self.artist = artist
        self.title = title
        self.genre_id = genre_id
        self.lyrics_id = lyrics_id

        # technical info fields
        self.date_time = date_time
        self.duration = duration

    def __repr__(self):
        return "<Audio(artist='{}', title='{}', duration='{}')>".format(
            self.artist, self.title, self.duration
        )

    def __str__(self):
        return "Audio called '{}'".format(
            VKAudio.FILE_NAME_FORMAT.format(**self.__dict__)
        )

    @classmethod
    def key(cls):
        return 'audio'

    def download(self, path: str):
        audio_file_subdirs = self.get_file_subdirs()
        check_dir(path, *audio_file_subdirs)

        audio_file_dir = os.path.join(path, *audio_file_subdirs)
        audio_file_name = self.get_file_name()
        audio_file_path = os.path.join(audio_file_dir, audio_file_name)

        download(self.link, audio_file_path)

    def get_file_subdirs(self) -> List[str]:
        audio_file_subdirs = [self.artist]
        return audio_file_subdirs

    def get_file_name(self) -> str:
        file_name = VKAudio.FILE_NAME_FORMAT.format(
            **self.__dict__
        )[:MAX_FILE_NAME_LEN - len(VKAudio.FILE_EXTENSION)].replace(os.sep, ' ') + VKAudio.FILE_EXTENSION
        return file_name

    @classmethod
    def from_raw(cls, raw_vk_object: dict) -> VKObject:
        return cls(
            owner_id=int(raw_vk_object['owner_id']),
            object_id=int(raw_vk_object['id']),
            artist=raw_vk_object['artist'].strip(),
            title=raw_vk_object['title'].strip(),
            duration=(
                datetime.min + timedelta(
                    seconds=int(raw_vk_object['duration'])
                )
            ).time(),
            date_time=datetime.fromtimestamp(int(raw_vk_object['date'])),
            genre_id=int(raw_vk_object.pop('genre_id', 0)),
            lyrics_id=int(raw_vk_object.pop('lyrics_id', 0)),
            link=raw_vk_object['url'] or None
        )


class VKVideo(VKAttachment):
    def __init__(self, owner_id: int, object_id: int, title: str, description: str, duration: time, date_time: datetime,
                 views_count: int, player: str, link: str, adding_date: datetime = None):
        super().__init__(owner_id, object_id, link)

        # info fields
        self.title = title
        self.description = description

        # technical info fields
        self.duration = duration
        self.date_time = date_time
        self.adding_date = adding_date
        self.views_count = views_count
        self.player = player

    def __repr__(self):
        return "<Video(title='{}', duration={})>".format(self.title, self.duration)

    def __str__(self):
        return "Video called '{}'".format(self.title)

    @classmethod
    def key(cls):
        return 'video'

    def download(self, path: str):
        video_file_subdirs = self.get_file_subdirs()
        check_dir(path, *video_file_subdirs)

        video_file_dir = os.path.join(path, *video_file_subdirs)
        video_file_name = self.get_file_name()
        video_file_path = os.path.join(video_file_dir, video_file_name)

        download(self.link, video_file_path)

    def get_file_subdirs(self) -> List[str]:
        doc_file_subdirs = []
        return doc_file_subdirs

    def get_file_name(self) -> str:
        file_name = self.title
        return file_name

    @classmethod
    def from_raw(cls, raw_vk_object: dict) -> VKObject:
        return cls(
            owner_id=int(raw_vk_object['owner_id']),
            object_id=int(raw_vk_object['id']),
            title=raw_vk_object['title'].strip(),
            description=raw_vk_object['description'] or None,
            duration=(
                datetime.min + timedelta(
                    seconds=int(raw_vk_object['duration'])
                )
            ).time(),
            date_time=datetime.fromtimestamp(int(raw_vk_object['date'])),
            adding_date=datetime.fromtimestamp(int(raw_vk_object['adding_date'])),
            views_count=int(raw_vk_object['views']),
            player=raw_vk_object['player'],
            link=VKVideo.get_link(raw_vk_object)
        )

    @staticmethod
    def get_link(raw_video: dict) -> str:
        photo_links = raw_video.get('files', dict())
        photo_links_keys = list(photo_links.keys())
        photo_links_keys.sort(
            key=lambda x: int(
                re.sub(r'\D+', '0', x.split('_')[-1])
            )
        )

        highest_res_link_key = photo_links_keys[-1]
        highest_res_link = photo_links[highest_res_link_key]

        return highest_res_link


class VKDoc(VKAttachment):
    def __init__(self, owner_id: int, object_id: int, title: str, size: int, ext: str, link: str):
        super().__init__(owner_id, object_id, link)

        # info fields
        self.title = title

        # technical info fields
        self.size = size
        self.ext = ext

    def __repr__(self):
        return "<Doc(title='{}', ext='{}')>".format(
            self.title, self.ext
        )

    def __str__(self):
        return "Doc called '{}'".format(self.title)

    @classmethod
    def key(cls):
        return 'doc'

    def download(self, path: str):
        doc_file_subdirs = self.get_file_subdirs()
        check_dir(path, *doc_file_subdirs)

        doc_file_dir = os.path.join(path, *doc_file_subdirs)
        doc_file_name = self.get_file_name()
        doc_file_path = os.path.join(doc_file_dir, doc_file_name)

        download(self.link, doc_file_path)

    def get_file_subdirs(self) -> List[str]:
        doc_file_subdirs = [self.ext]
        return doc_file_subdirs

    def get_file_name(self) -> str:
        file_name = self.title
        return file_name

    @classmethod
    def from_raw(cls, raw_vk_object: dict) -> VKObject:
        return cls(
            owner_id=int(raw_vk_object['owner_id']),
            object_id=int(raw_vk_object['id']),
            title=raw_vk_object['title'].strip(),
            size=raw_vk_object['size'],
            ext=raw_vk_object['ext'],
            link=raw_vk_object['url'] or None
        )
