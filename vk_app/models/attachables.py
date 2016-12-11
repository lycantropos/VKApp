import re
from datetime import datetime, time, timedelta
from typing import List, Dict, Any

from vk_app.models.objects import VKAttachable, VKFileAttachable
from vk_app.utils import get_normalized_file_name

__all__ = ['VKPage', 'VKDoc', 'VKNote', 'VKPoll', 'VKPhotoAlbum',
           'VKSticker', 'VKPhoto', 'VKAudio', 'VKVideo']


class VKPage(VKAttachable):
    """
    Implements working with VK wiki-pages

    more info about `Page` objects at https://vk.com/dev/page
    """

    def __init__(self, owner_id: int, object_id: int, creator_id: int, title: str,
                 html: str, who_can_view: int, who_can_edit: int, date_time: datetime,
                 edited_date_time: datetime, views_count: int, source: str = None):
        super().__init__(owner_id, object_id)

        # VK utility fields
        self.creator_id = creator_id

        # info fields
        self.title = title
        self.who_can_view = who_can_view
        self.who_can_edit = who_can_edit

        # technical info fields
        self.date_time = date_time
        self.edited_date_time = edited_date_time
        self.views_count = views_count
        self.html = html
        self.source = source

    @classmethod
    def key(cls):
        return 'page'

    @classmethod
    def from_raw(cls, raw_vk_object: Dict[str, Any]) -> 'VKPage':
        return cls(
            owner_id=-raw_vk_object['group_id'],
            object_id=raw_vk_object['id'],
            creator_id=raw_vk_object.get('creator_id'),
            title=raw_vk_object['title'],
            who_can_view=raw_vk_object['who_can_view'],
            who_can_edit=raw_vk_object['who_can_edit'],
            date_time=datetime.utcfromtimestamp(raw_vk_object['created']),
            edited_date_time=datetime.utcfromtimestamp(raw_vk_object['edited']),
            views_count=raw_vk_object['views'],
            html=raw_vk_object['html'],
            source=raw_vk_object.get('source', None),
        )


class VKNote(VKAttachable):
    """
    Implements working with VK notes

    more info about `Note` objects at https://vk.com/dev/note
    """

    def __init__(self, owner_id: int, object_id: int, title: str, date_time: datetime,
                 comments_count: int, text: str = None):
        super().__init__(owner_id, object_id)

        # info fields
        self.title = title
        self.text = text

        # technical info fields
        self.date_time = date_time
        self.comments_count = comments_count

    @classmethod
    def key(cls):
        return 'note'

    @classmethod
    def from_raw(cls, raw_vk_object: Dict[str, Any]) -> 'VKNote':
        return cls(
            owner_id=raw_vk_object['owner_id'],
            object_id=raw_vk_object['id'],
            title=raw_vk_object['title'],
            text=raw_vk_object.get('text', None),
            date_time=datetime.utcfromtimestamp(raw_vk_object['date']),
            comments_count=raw_vk_object['comments'],
        )


class VKPoll(VKAttachable):
    """
    Implements working with VK polls

    more info about `Poll` objects at https://vk.com/dev/polls.getById
    """

    def __init__(self, owner_id: int, object_id: int, question: str, answers: List[dict],
                 anonymous: bool, date_time: datetime, votes_count: int):
        super().__init__(owner_id, object_id)

        # info fields
        self.question = question
        self.answers = answers
        self.anonymous = anonymous

        # technical info fields
        self.date_time = date_time
        self.votes_count = votes_count

    @classmethod
    def key(cls):
        return 'poll'

    @classmethod
    def from_raw(cls, raw_vk_object: Dict[str, Any]) -> 'VKPoll':
        return cls(
            owner_id=raw_vk_object['owner_id'],
            object_id=raw_vk_object['id'],
            question=raw_vk_object['question'].strip(),
            answers=raw_vk_object['answers'],
            anonymous=raw_vk_object['anonymous'] == 1,
            date_time=datetime.utcfromtimestamp(raw_vk_object['created']),
            votes_count=raw_vk_object['votes']
        )


class VKPhotoAlbum(VKAttachable):
    """
    Implements working with VK photo albums

    more info about `Photo album` objects at https://vk.com/dev/photos.getAlbums
    """

    def __init__(self, owner_id: int, object_id: int, title: str, date_time: datetime,
                 updated_date_time: datetime, photos_count: int, description: str = None):
        super().__init__(owner_id, object_id)

        # info fields
        self.title = title
        self.description = description

        # technical info fields
        self.date_time = date_time
        self.updated_date_time = updated_date_time
        self.photos_count = photos_count

    @classmethod
    def key(cls):
        return 'album'

    @classmethod
    def from_raw(cls, raw_vk_object: Dict[str, Any]) -> 'VKPhotoAlbum':
        return cls(
            owner_id=raw_vk_object['owner_id'],
            object_id=raw_vk_object['id'],
            title=raw_vk_object['title'],
            description=raw_vk_object['description'] or None,
            date_time=datetime.utcfromtimestamp(raw_vk_object['created']),
            updated_date_time=datetime.utcfromtimestamp(raw_vk_object['updated']),
            photos_count=raw_vk_object['size']
        )


def get_photo_link(raw_object: Dict[str, Any]) -> str:
    """Returns highest resolution link for photo-like attachable ('photo', 'sticker')"""
    photo_link_keys = list(
        raw_photo_key
        for raw_photo_key in raw_object
        if raw_photo_key.startswith('photo')
    )
    photo_link_keys.sort(key=link_key_sort_key)

    highest_res_link_key = photo_link_keys[-1]
    highest_res_link = raw_object[highest_res_link_key]

    return highest_res_link


def link_key_sort_key(link_key: str):
    return int(re.sub(r'\D', '0', link_key.split('_')[-1]))


class VKSticker(VKFileAttachable):
    """
    Implements working with VK stickers

    more info about `Sticker` objects at https://vk.com/dev/attachments_m
    """

    def __init__(self, owner_id: int, object_id: int,
                 height: int, width: int,
                 link: str):
        super().__init__(owner_id, object_id)

        # technical info fields
        self.width = width
        self.height = height
        self.link = link

    @classmethod
    def key(cls):
        return 'sticker'

    @classmethod
    def from_raw(cls, raw_vk_object: Dict[str, Any]) -> 'VKSticker':
        # stickers are supplied in packs,
        # each pack is a product,
        # so product id is picked as owner id of given sticker
        return cls(
            owner_id=raw_vk_object['product_id'],
            object_id=raw_vk_object['id'],
            height=raw_vk_object['height'],
            width=raw_vk_object['width'],
            link=get_photo_link(raw_vk_object)
        )


class VKPhoto(VKFileAttachable):
    """
    Implements working with VK photos

    more info about `Photo` objects at https://vk.com/dev/photo
    """

    def __init__(self, owner_id: int, object_id: int, album_id: int, album: str,
                 date_time: datetime, user_id: int = None, text: str = None,
                 link: str = None):
        super().__init__(owner_id, object_id, link)

        # VK utility fields
        self.user_id = user_id

        # info fields
        self.album_id = album_id
        self.album = album
        self.text = text

        # technical info fields
        self.date_time = date_time

    @classmethod
    def key(cls) -> str:
        return 'photo'

    def get_file_name(self, **kwargs) -> str:
        image_name = self.vk_id
        image_name = get_normalized_file_name(image_name, self.get_file_extension(**kwargs))
        return image_name

    def get_file_extension(self, **kwargs) -> str:
        return '.png' if 'marked' in kwargs and kwargs['marked'] is True else '.jpg'

    @classmethod
    def from_raw(cls, raw_photo: Dict[str, Any]) -> 'VKPhoto':
        return cls(
            owner_id=raw_photo['owner_id'],
            object_id=raw_photo['id'],
            user_id=raw_photo.get('user_id', None),
            album_id=raw_photo['album_id'],
            album=SPECIAL_ALBUMS_IDS_TITLES.get(raw_photo['album_id'], None),
            text=raw_photo['text'] or None,
            date_time=datetime.utcfromtimestamp(raw_photo['date']),
            link=get_photo_link(raw_photo)
        )

    @classmethod
    def getUploadServer_method(cls, dst_type: str) -> str:
        if dst_type == 'default':
            return 'photos.getUploadServer'
        elif dst_type == 'owner':
            return 'photos.getOwnerPhotoUploadServer'
        elif dst_type == 'wall':
            return 'photos.getWallUploadServer'
        elif dst_type == 'message':
            return 'photos.getMessagesUploadServer'
        elif dst_type == 'chat':
            return 'photos.getChatUploadServer'
        elif dst_type == 'market':
            return 'photos.getMarketUploadServer'
        elif dst_type == 'market_album':
            return 'photos.getMarketAlbumUploadServer'
        else:
            raise ValueError('Unknown photo uploading destination type: {}'.format(dst_type))

    @classmethod
    def save_method(cls, dst_type: str) -> str:
        if dst_type == 'default':
            return 'photos.save'
        elif dst_type == 'owner':
            return 'photos.saveOwnerPhoto'
        elif dst_type == 'wall':
            return 'photos.saveWallPhoto'
        elif dst_type == 'message':
            return 'photos.saveMessagesPhoto'
        elif dst_type == 'chat':
            return 'messages.setChatPhoto'
        elif dst_type == 'market':
            return 'photos.saveMarketPhoto'
        elif dst_type == 'market_album':
            return 'photos.saveMarketAlbumPhoto'
        else:
            raise ValueError('Unknown photo uploading destination type: {}'.format(dst_type))


SPECIAL_ALBUMS_IDS_TITLES = {
    -6: 'profile',
    -7: 'wall',
    -15: 'saved',
    -23: 'graffiti'
}


class VKAudio(VKFileAttachable):
    """
    Implements working with VK audios

    more info about `Audio` objects at https://vk.com/dev/audio_object
    """
    FILE_NAME_FORMAT = '{self.artist} - {self.title}'

    def __init__(self, owner_id: int, object_id: int, artist: str, title: str, duration: time,
                 date_time: datetime, genre: str = None, lyrics_id: int = None,
                 link: str = None):
        super().__init__(owner_id, object_id, link)

        # info fields
        self.artist = artist
        self.title = title
        self.genre = genre
        self.lyrics_id = lyrics_id

        # technical info fields
        self.date_time = date_time
        self.duration = duration

    @classmethod
    def key(cls) -> str:
        return 'audio'

    def get_file_name(self, **kwargs) -> str:
        audio_file_name = VKAudio.FILE_NAME_FORMAT.format(self=self)
        audio_file_name = get_normalized_file_name(audio_file_name, self.get_file_extension())
        return audio_file_name

    def get_file_extension(self, **kwargs) -> str:
        return '.mp3'

    @classmethod
    def from_raw(cls, raw_vk_object: Dict[str, Any]) -> 'VKAudio':
        return cls(
            owner_id=raw_vk_object['owner_id'],
            object_id=raw_vk_object['id'],
            artist=raw_vk_object['artist'].strip(),
            title=raw_vk_object['title'].strip(),
            duration=(datetime.min + timedelta(seconds=raw_vk_object['duration'])).time(),
            date_time=datetime.utcfromtimestamp(raw_vk_object['date']),
            genre=AUDIO_GENRES_IDS_GENRES.get(raw_vk_object.get('genre_id'), None),
            lyrics_id=raw_vk_object.get('lyrics_id', None),
            link=raw_vk_object['url'] or None
        )

    @classmethod
    def getUploadServer_method(cls, dst_type: str = None) -> str:
        return 'audio.getUploadServer'

    @classmethod
    def save_method(cls, dst_type: str = None) -> str:
        return 'audio.save'


AUDIO_GENRES_IDS_GENRES = {
    1: 'Rock',
    2: 'Pop',
    3: 'Rap & Hip-Hop',
    4: 'Easy Listening',
    5: 'Dance & House',
    6: 'Instrumental',
    7: 'Metal',
    21: 'Alternative',
    8: 'Dubstep',
    1001: 'Jazz & Blues',
    10: 'Drum & Bass',
    11: 'Trance',
    12: 'Chanson',
    13: 'Ethnic',
    14: 'Acoustic & Vocal',
    15: 'Reggae',
    16: 'Classical',
    17: 'Indie Pop',
    19: 'Speech',
    22: 'Electropop & Disco',
    18: 'Other'
}


class VKVideo(VKFileAttachable):
    """
    Implements working with VK videos

    more info about `Video` objects at https://vk.com/dev/video_object
    """

    def __init__(self, owner_id: int, object_id: int, title: str, description: str,
                 duration: time, date_time: datetime, views_count: int,
                 adding_date: datetime = None, access_key: str = None,
                 player_link: str = None, link: str = None):
        super().__init__(owner_id, object_id, link)

        # info fields
        self.title = title
        self.description = description

        # technical info fields
        self.duration = duration
        self.date_time = date_time
        self.adding_date = adding_date
        self.access_key = access_key
        self.views_count = views_count
        self.player_link = player_link

    @classmethod
    def key(cls) -> str:
        return 'video'

    def get_file_name(self, **kwargs) -> str:
        video_file_name = self.title
        video_file_name = get_normalized_file_name(video_file_name,
                                                   ext=self.get_file_extension())
        return video_file_name

    def get_file_extension(self, **kwargs) -> str:
        return '.mp4'

    @classmethod
    def from_raw(cls, raw_vk_object: Dict[str, Any]) -> 'VKVideo':
        return cls(
            owner_id=raw_vk_object['owner_id'],
            object_id=raw_vk_object['id'],
            title=raw_vk_object['title'].strip(),
            description=raw_vk_object['description'] or None,
            duration=(datetime.min + timedelta(seconds=raw_vk_object['duration'])).time(),
            date_time=datetime.utcfromtimestamp(raw_vk_object['date']),
            adding_date=datetime.utcfromtimestamp(raw_vk_object['adding_date'])
            if 'adding_date' in raw_vk_object else None,
            access_key=raw_vk_object.get('access_key'),
            views_count=raw_vk_object['views'],
            **cls.get_links(raw_vk_object)
        )

    @staticmethod
    def get_links(raw_video: dict) -> Dict[str, str]:
        links = raw_video.get('files', dict())
        player_link = links.get('external') or raw_video.get('player')
        links_keys = list(links.keys())
        links_keys.sort(key=link_key_sort_key)

        link = links[links_keys[-1]] if links_keys else None

        return dict(link=link, player_link=player_link)

    @classmethod
    def getUploadServer_method(cls, dst_type: str = None) -> str:
        return 'video.save'

    @classmethod
    def save_method(cls, dst_type: str = None) -> str:
        return 'video.save'


class VKDoc(VKFileAttachable):
    """
    Implements working with VK documents

    more info about `Doc` objects at https://vk.com/dev/doc
    """

    def __init__(self, owner_id: int, object_id: int, title: str, size: int, ext: str,
                 link: str):
        super().__init__(owner_id, object_id, link)

        # info fields
        self.title = title

        # technical info fields
        self.size = size
        self.ext = ext

    @classmethod
    def key(cls) -> str:
        return 'doc'

    def get_file_name(self, **kwargs) -> str:
        file_name = get_normalized_file_name('.'.join(self.title.split('.')[:-1]), self.ext)
        return file_name

    def get_file_extension(self, **kwargs) -> str:
        return self.ext

    @classmethod
    def from_raw(cls, raw_vk_object: dict) -> 'VKDoc':
        return cls(
            owner_id=raw_vk_object['owner_id'],
            object_id=raw_vk_object['id'],
            title=raw_vk_object['title'].strip(),
            size=raw_vk_object['size'],
            ext=raw_vk_object['ext'],
            link=raw_vk_object['url'] or None
        )

    @classmethod
    def getUploadServer_method(cls, dst_type: str) -> str:
        if dst_type == 'default':
            return 'docs.getUploadServer'
        elif dst_type == 'wall':
            return 'docs.getWallUploadServer'
        else:
            raise ValueError('Unknown document uploading destination type: {}'.format(dst_type))

    @classmethod
    def save_method(cls, dst_type: str = None) -> str:
        return 'docs.save'
