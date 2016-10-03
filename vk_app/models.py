import os
import shutil
from datetime import datetime, time, timedelta
from typing import List, Dict

from vk_app.services.loading import download
from vk_app.utils import find_file, check_dir, get_year_month_date, get_valid_dirs

VK_ID_FORMAT = '{}_{}'


class VKObject:
    def __init__(self, owner_id: int, object_id: int, date_time: datetime):
        # VK utility fields
        self.vk_id = VK_ID_FORMAT.format(owner_id, object_id)
        self.owner_id = owner_id
        self.object_id = object_id

        # technical info fields
        self.date_time = date_time

    def __eq__(self, other):
        if type(self) is type(other):
            return self.vk_id == other.vk_id and \
                   self.date_time == other.date_time
        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    @classmethod
    def from_raw(cls, raw_vk_object: dict) -> type:
        """Must be overridden by inheritors"""


class VKAttachment(VKObject):
    def __init__(self, owner_id: int, object_id: int, date_time: datetime, link: str):
        super().__init__(owner_id, object_id, date_time)

        # technical info fields
        self.link = link

    def __eq__(self, other):
        if type(self) is type(other):
            return self.vk_id == other.vk_id and \
                   self.date_time == other.date_time and \
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


class VKPhoto(VKAttachment):
    def __init__(self, owner_id: int, object_id: int, user_id: int, album: str, date_time: datetime, comment: str = '',
                 link: str = ''):
        super().__init__(owner_id, object_id, date_time, link)

        # VK utility fields
        self.user_id = user_id

        # info fields
        self.album = album
        self.comment = comment

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
        super().__init__(owner_id, object_id, date_time, link)

        # info fields
        self.artist = artist
        self.title = title
        self.genre_id = genre_id
        self.lyrics_id = lyrics_id

        # technical info fields
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


ATTACHMENTS_KEY_VK_OBJECT = dict(
    (inheritor.key(), inheritor)
    for inheritor in VKAttachment.__subclasses__()
)


class VKPost(VKObject):
    def __init__(self, owner_id: int, object_id: int, from_id: int, created_by: int,
                 comment: str, attachments: Dict[str, List[VKAttachment]], date_time: datetime,
                 likes_count: int, reposts_count: int, comments_count: int):
        super().__init__(owner_id, object_id, date_time)

        # VK utility fields
        self.from_id = from_id
        self.created_by = created_by

        # info fields
        self.comment = comment
        self.attachments = attachments

        # technical info fields
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
