import unittest
from datetime import datetime, time

from models.attachments import VKPhoto, VKAudio, VKVideo
from models.post import VKPost


class TestModels(unittest.TestCase):
    def setUp(self):
        self.raw_photo = dict(
            id=278184324,
            album_id=-6,
            owner_id=1,
            photo_75='https://pp.vk.me/c10408/u4172580/-6/s_24887a5a.jpg',
            photo_130='https://pp.vk.me/c10408/u4172580/-6/m_79ab6f4a.jpg',
            photo_604='https://pp.vk.me/c10408/u4172580/-6/x_ee97448e.jpg',
            text='',
            date=1328126422,
            post_id=45430,
            likes={
                'user_likes': 0,
                'count': 577904
            },
            comments={
                'count': 421
            },
            can_comment=1,
            can_repost=1,
            tags={
                'count': 0
            }
        )
        self.photo = VKPhoto(
            owner_id=1, object_id=278184324, user_id=0, album=None,
            date_time=datetime(2012, 2, 2, 3, 0, 22), comment='',
            link='https://pp.vk.me/c10408/u4172580/-6/x_ee97448e.jpg'
        )
        self.raw_audio = dict(
            id=456239153,
            owner_id=33151248,
            artist="Blink 182",
            title="I'm Lost Without You",
            duration=189,
            date=1475376942,
            url='https://psv4.vk.me/c4405/u729766/audios/e827863eec4b.mp3?extra='
                'boaG2GtdV78oAJzBtTlyr9ko3pue4CpcY9MiirqedU5LbqHOYLxm9_m1Tu_fB1uG-'
                'Xc78dRNLLIK2--1MjiK91MW0nV-g3C77CI0JIUmfpHXImJ0_PUC77pWCeBIEWc3ii-ajmFXXxc',
            lyrics_id=11814435,
            genre_id=1
        )
        self.audio = VKAudio(
            owner_id=33151248, object_id=456239153, artist="Blink 182", title="I'm Lost Without You",
            duration=time(0, 3, 9), date_time=datetime(2016, 10, 2, 9, 55, 42), genre_id=1, lyrics_id=11814435,
            link='https://psv4.vk.me/c4405/u729766/audios/e827863eec4b.mp3?extra='
                 'boaG2GtdV78oAJzBtTlyr9ko3pue4CpcY9MiirqedU5LbqHOYLxm9_m1Tu_fB1uG-'
                 'Xc78dRNLLIK2--1MjiK91MW0nV-g3C77CI0JIUmfpHXImJ0_PUC77pWCeBIEWc3ii-ajmFXXxc'
        )

        self.raw_video = dict(
            id=170594858,
            owner_id=33151248,
            title="Grouplove - I'm With You [Official Music Video]",
            duration=330,
            description='',
            date=1415048962,
            views=221,
            comments=0,
            photo_130='https://pp.vk.me/c543305/u234346085/video/s_c84862b9.jpg',
            photo_320='https://pp.vk.me/c543305/u234346085/video/l_fb558594.jpg',
            adding_date=1415048962,
            files=dict(
                mp4_240='https://cs543305.vk.me/u234346085/videos/29dfb3e3d8.240.mp4?extra='
                        'XngTjD0nYtvFXmjf7xzcujLkgw5kNUlXTL1xTjbToBnKF2J_Qaj'
                        '-ZzFC_XXWAid_-6qSn1iW75kysTYVN-cz53p52MDo_nFar-n64fK4wVTPr1_qeiIz8ZE3h9ME6TlApGtGpNYhcA',
                mp4_360='https://cs543305.vk.me/u234346085/videos/29dfb3e3d8.360.mp4?extra='
                        'XngTjD0nYtvFXmjf7xzcujLkgw5kNUlXTL1xTjbToBnKF2J_Qaj'
                        '-ZzFC_XXWAid_-6qSn1iW75kysTYVN-cz53p52MDo_nFar-n64fK4wVTPr1_qeiIz8ZE3h9ME6TlApGtGpNYhcA',
                mp4_480='https://cs543305.vk.me/u234346085/videos/29dfb3e3d8.480.mp4?extra='
                        'XngTjD0nYtvFXmjf7xzcujLkgw5kNUlXTL1xTjbToBnKF2J_Qaj'
                        '-ZzFC_XXWAid_-6qSn1iW75kysTYVN-cz53p52MDo_nFar-n64fK4wVTPr1_qeiIz8ZE3h9ME6TlApGtGpNYhcA',
                mp4_720='https://cs543305.vk.me/u234346085/videos/29dfb3e3d8.720.mp4?extra='
                        'XngTjD0nYtvFXmjf7xzcujLkgw5kNUlXTL1xTjbToBnKF2J_Qaj'
                        '-ZzFC_XXWAid_-6qSn1iW75kysTYVN-cz53p52MDo_nFar-n64fK4wVTPr1_qeiIz8ZE3h9ME6TlApGtGpNYhcA'
            ),
            player='https://vk.com/video_ext.php?oid=33151248&id=170594858&hash=6af70b680de137f8&__ref='
                   'vk.api&api_hash=1475515983cb93631fcefce81573_GMZTCNJRGI2DQ',
            can_edit=1,
            can_add=1,
            privacy_view=['all'],
            privacy_comment=['all'],
            can_comment=1,
            can_repost=1,
            likes=dict(
                user_likes=0,
                count=1
            ),
            reposts=dict(
                count=0,
                user_reposted=0
            ),
            repeat=0
        )
        self.video = VKVideo(
            owner_id=33151248, object_id=170594858, title="Grouplove - I'm With You [Official Music Video]",
            description=None, duration=time(0, 5, 30), date_time=datetime(2014, 11, 4, 3, 9, 22), views_count=221,
            player='https://vk.com/video_ext.php?oid=33151248&id=170594858&hash=6af70b680de137f8&__ref='
                   'vk.api&api_hash=1475515983cb93631fcefce81573_GMZTCNJRGI2DQ',
            link='https://cs543305.vk.me/u234346085/videos/29dfb3e3d8.720.mp4?extra='
                 'XngTjD0nYtvFXmjf7xzcujLkgw5kNUlXTL1xTjbToBnKF2J_Qaj'
                 '-ZzFC_XXWAid_-6qSn1iW75kysTYVN-cz53p52MDo_nFar-n64fK4wVTPr1_qeiIz8ZE3h9ME6TlApGtGpNYhcA',
            adding_date=datetime(2014, 11, 4, 3, 9, 22)
        )

        self.raw_post = dict(
            post_source={'type': 'vk'}, comments={'can_post': 0, 'count': 0}, can_edit=1, date=1475254508,
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                 "Nulla sit amet leo magna. Etiam convallis metus in mollis ultrices. "
                 "In purus velit, vehicula ut turpis sit amet, faucibus mollis nibh. "
                 "Duis dolor tellus, malesuada eget pellentesque et, pellentesque sed ante. "
                 "Ut tincidunt lacus et vulputate commodo. "
                 "Fusce eu nunc semper, vulputate eros commodo, lacinia diam. "
                 "Vestibulum semper justo at nisl tempus pellentesque. "
                 "Proin sed ultrices elit, eu viverra metus. "
                 "Vestibulum bibendum ornare finibus. "
                 "Fusce luctus in metus et fermentum. "
                 "Aenean non tortor risus.",
            can_delete=1, attachments=[
                {
                    'photo': {'user_id': 33151248, 'post_id': 1,
                              'photo_130': 'https://pp.vk.me/c638122/v638122248/1c3d/xZ5aqUDcybM.jpg',
                              'text': '', 'width': 1600,
                              'access_key': '4f4e6ad518a7cf7ef7', 'height': 1185,
                              'photo_1280': 'https://pp.vk.me/c638122/v638122248/1c40/-RO1oEMK20Y.jpg',
                              'photo_75': 'https://pp.vk.me/c638122/v638122248/1c3c/p6jM2c9WYpg.jpg',
                              'id': 431928280,
                              'photo_604': 'https://pp.vk.me/c638122/v638122248/1c3e/VAh115dZjgk.jpg',
                              'photo_2560': 'https://pp.vk.me/c638122/v638122248/1c41/SnfoaFP-Hfk.jpg',
                              'album_id': -7, 'owner_id': -129836227,
                              'photo_807': 'https://pp.vk.me/c638122/v638122248/1c3f/YfqUONQeVe0.jpg',
                              'date': 1475254507}, 'type': 'photo'
                }
            ],
            reposts={'user_reposted': 0, 'count': 0},
            from_id=-129836227, id=1, post_type='post', created_by=33151248,
            can_pin=1, marked_as_ads=0, owner_id=-129836227,
            likes={'user_likes': 0, 'can_publish': 1, 'count': 0, 'can_like': 1}
        )
        self.post = VKPost(
            owner_id=-129836227, object_id=1, from_id=-129836227, created_by=33151248,
            comment="Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                    "Nulla sit amet leo magna. "
                    "Etiam convallis metus in mollis ultrices. "
                    "In purus velit, vehicula ut turpis sit amet, "
                    "faucibus mollis nibh. "
                    "Duis dolor tellus, malesuada eget pellentesque et, pellentesque sed ante. "
                    "Ut tincidunt lacus et vulputate commodo. "
                    "Fusce eu nunc semper, vulputate eros commodo, lacinia diam. "
                    "Vestibulum semper justo at nisl tempus pellentesque. "
                    "Proin sed ultrices elit, eu viverra metus. "
                    "Vestibulum bibendum ornare finibus. "
                    "Fusce luctus in metus et fermentum. "
                    "Aenean non tortor risus.",
            attachments=dict(
                photo=[
                    VKPhoto(
                        owner_id=-129836227, object_id=431928280, user_id=33151248, album=None,
                        date_time=datetime(2016, 9, 30, 23, 55, 7), comment='',
                        link='https://pp.vk.me/c638122/v638122248/1c41/SnfoaFP-Hfk.jpg'
                    )
                ]
            ),
            date_time=datetime(2016, 9, 30, 23, 55, 8),
            likes_count=0, reposts_count=0, comments_count=0
        )

    def test_vk_photo_from_raw(self):
        self.assertEqual(VKPhoto.from_raw(self.raw_photo), self.photo)

    def test_vk_audio_from_raw(self):
        self.assertEqual(VKAudio.from_raw(self.raw_audio), self.audio)

    def test_vk_video_from_raw(self):
        video = VKVideo.from_raw(self.raw_video)
        self.assertEqual(video, self.video, 'Test message')

    def test_vk_post_from_raw(self):
        self.assertEqual(VKPost.from_raw(self.raw_post), self.post)


if __name__ == '__main__':
    test = TestModels()
    test.run()
