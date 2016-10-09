import datetime
import unittest

from vk_app import App
from vk_app.models.attachments import VKAudio, VKDoc, VKNote, VKPhoto, VKPoll, VKVideo
from vk_app.models.post import VKPost


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.owner_id = -129836227
        self.wall_posts = [
            VKPost(
                owner_id=-129836227, object_id=2, from_id=-129836227, created_by=0,
                text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                     "Nulla sit amet leo magna. "
                     "Etiam convallis metus in mollis ultrices. "
                     "In purus velit, vehicula ut turpis sit amet, faucibus mollis nibh. "
                     "Duis dolor tellus, malesuada eget pellentesque et, pellentesque sed ante. "
                     "Ut tincidunt lacus et vulputate commodo. "
                     "Fusce eu nunc semper, vulputate eros commodo, lacinia diam. "
                     "Vestibulum semper justo at nisl tempus pellentesque. "
                     "Proin sed ultrices elit, eu viverra metus. "
                     "Vestibulum bibendum ornare finibus. "
                     "Fusce luctus in metus et fermentum. "
                     "Aenean non tortor risus.",
                attachments=list(), date_time=datetime.datetime(2016, 9, 30, 23, 56, 8),
                likes_count=0, reposts_count=0, comments_count=0
            ),
            VKPost(
                owner_id=-129836227, object_id=1, from_id=-129836227, created_by=0,
                text='',
                attachments=[
                    dict(
                        photo=
                        VKPhoto(
                            owner_id=-129836227, object_id=431928280, album_id=-7,
                            album='wall',
                            date_time=datetime.datetime(2016, 9, 30, 23, 55, 7), user_id=100,
                            text=None,
                            link='http://cs638122.vk.me/v638122248/1c41/SnfoaFP-Hfk.jpg')
                    )
                ],
                date_time=datetime.datetime(2016, 9, 30, 23, 55, 8), likes_count=0,
                reposts_count=0, comments_count=0
            )
        ]
        self.posts_ids = '90353483_117'
        self.posts_by_ids = [
            VKPost(
                owner_id=90353483, object_id=117, from_id=90353483, created_by=0, text='Good ones?',
                attachments=[
                    dict(
                        photo=VKPhoto(
                            owner_id=90353483, object_id=441807821, album_id=-7, album='wall',
                            date_time=datetime.datetime(2016, 10, 7, 21, 10, 48), user_id=None, text=None,
                            link='http://cs638916.vk.me/v638916483/3238/ffB6PdgQUh8.jpg'
                        )
                    ),
                    dict(
                        video=VKVideo(
                            owner_id=90353483, object_id=456239017, title='1000 MPH - by Ok Go',
                            description='A music video for "1000 MPH" by Ok Go, showing their adventures on tour',
                            duration=datetime.time(0, 3, 37),
                            date_time=datetime.datetime(2016, 10, 7, 21, 0, 50),
                            views_count=25, adding_date=None, player_link=None, link=None
                        )
                    ),
                    dict(
                        video=VKVideo(
                            owner_id=-18249587, object_id=145823149, title='OK Go - 1000 Miles Per Hour',
                            description=None, duration=datetime.time(0, 3, 35),
                            date_time=datetime.datetime(2010, 6, 20, 6, 19, 41), views_count=137,
                            adding_date=None,
                            player_link=None, link=None
                        )
                    ),
                    dict(
                        audio=VKAudio(
                            owner_id=2000021658, object_id=456239096, artist='OK Go',
                            title='1000 Miles Per Hour',
                            duration=datetime.time(0, 3, 33),
                            date_time=datetime.datetime(2016, 10, 7, 21, 12, 41), genre='Other',
                            lyrics_id=3571070,
                            link='http://cs4-1v4.vk-cdn.net/p20/618d6733af8701.mp3?extra='
                                 '028FbtjHGd7fbygDV0mNY_AD3UR_jINZzRjbUqhItr_'
                                 'iAvcy3LUCL78QRo1wpadyxoADjcEwc8Wp1STBe4saevj2173UPE8Ox'
                                 '-7WvZxmSXVuXXRa_Sby2dquRaKP7w'
                        )
                    ),
                    dict(
                        doc=VKDoc(
                            owner_id=90353483, object_id=438149776, title='OK Go - 1000 Miles Per Hour.txt',
                            size=885, ext='txt',
                            link='https://vk.com/doc90353483_438149776?hash='
                                 '65b13f2ac27cc30a5e&dl=1475897690226c0d6fee413dec4a&api=1'
                        )
                    ),
                    dict(
                        note=VKNote(
                            owner_id=90353483, object_id=11771661, title='OK Go - 1000 Miles Per Hour',
                            date_time=datetime.datetime(2016, 10, 7, 21, 10, 54), comments_count=0,
                            text=None
                        )
                    ),
                    dict(
                        poll=VKPoll(
                            owner_id=90353483, object_id=240627317, question='Good ones?',
                            answers=[{'text': 'ofc', 'votes': 1, 'rate': 100.0, 'id': 803133258}], anonymous=False,
                            date_time=datetime.datetime(2016, 10, 7, 21, 12, 41), votes_count=1
                        )
                    )
                ],
                date_time=datetime.datetime(2016, 10, 7, 21, 12, 39), likes_count=0, reposts_count=0,
                comments_count=0
            )
        ]

    def test_vk_api_wall_get(self):
        raw_posts = self.app.api_session.wall.get(owner_id=self.owner_id)['items']
        posts = list(VKPost.from_raw(raw_post) for raw_post in raw_posts)
        self.assertListEqual(posts, self.wall_posts)

    def test_vk_api_wall_getById(self):
        raw_posts = self.app.api_session.wall.getById(posts=self.posts_ids)
        posts = list(VKPost.from_raw(raw_post) for raw_post in raw_posts)
        self.assertListEqual(posts, self.posts_by_ids)
