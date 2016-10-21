import datetime
import unittest

from vk_app.attachables import VKAudio, VKDoc, VKNote, VKPhoto, VKPoll, VKVideo
from vk_app.post import VKPost
from vk_app import App


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.owner_id = -129836227
        self.wall_posts = [
            VKPost(
                owner_id=-129836227, object_id=5, from_id=-129836227, created_by=0,
                   text=(
                       'Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
                       'Fusce vel elit congue, tempus velit nec, viverra leo. '
                       'Sed pulvinar aliquet consequat. '
                       'Sed in nunc turpis. '
                       'Suspendisse molestie nisi sed rhoncus molestie. '
                       'Morbi id tortor ut urna viverra volutpat at a sapien. '
                       'Fusce ac odio et dui varius sagittis. '
                       'Aliquam tempus sollicitudin leo, non dictum massa ullamcorper id. '
                       'Mauris non enim at orci vehicula tristique vitae sollicitudin odio. '
                       'Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. '
                       'Integer tincidunt eleifend tellus et accumsan. '
                       'Curabitur pellentesque aliquet sapien. '
                       'Suspendisse egestas feugiat congue. '
                       'Sed id pharetra massa. '
                       'Fusce vitae aliquam mi. '
                       'Sed aliquet, nibh eget vehicula cursus, mauris neque porttitor lectus, '
                       'in aliquam arcu arcu in ex.\n'
                       '\n'
                       'Donec dapibus justo nec purus euismod, nec accumsan lorem maximus. '
                       'Phasellus et sem quam. '
                       'Nunc ipsum sapien, malesuada id velit pellentesque, mollis pellentesque est. '
                       'Morbi elementum sagittis vulputate. '
                       'Cras ipsum justo, facilisis ac vulputate nec, sollicitudin vel neque. '
                       'Curabitur varius consequat neque sit amet laoreet. '
                       'Suspendisse eget fermentum felis, eu venenatis augue. '
                       'Nullam et eros quis justo rhoncus molestie. '
                       'Interdum et malesuada fames ac ante ipsum primis in faucibus. '
                       'In ultricies feugiat massa, eget iaculis diam consequat a. '
                       'Fusce ut eros id massa fermentum venenatis. '
                       'Nam nisl ipsum, consequat vitae mollis et, scelerisque ac arcu. '
                       'Sed a sem semper lorem congue iaculis. '
                       'Curabitur imperdiet magna a lectus dignissim tristique. '
                       'Nunc condimentum libero blandit bibendum pellentesque.\n'
                       '\n'
                       'Quisque eu tellus eget odio vulputate aliquet. '
                       'In ac justo at nisi tempor pretium id sollicitudin leo. '
                       'Phasellus venenatis magna non urna ultricies placerat. '
                       'Fusce eget interdum ligula. '
                       'Sed turpis turpis, commodo non urna vel, congue ultrices dui. '
                       'Nullam ut tristique purus, et facilisis diam. '
                       'Vestibulum ultrices, velit et convallis semper, diam mi luctus massa, '
                       'ac cursus mi mauris quis augue. '
                       'Nam fringilla egestas fermentum. '
                       'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices '
                       'posuere cubilia Curae; Aliquam iaculis consectetur convallis.\n'
                       '\n'
                       'Fusce porta felis sit amet hendrerit laoreet. '
                       'Praesent ipsum lorem, iaculis ut vehicula eu, aliquet quis est. '
                       'Integer non est justo. '
                       'Vestibulum auctor consequat ex, vitae consectetur diam porta sit amet. '
                       'Nulla pretium fermentum velit, ac consectetur purus ultricies quis. '
                       'Curabitur vitae velit nec metus vulputate iaculis et ac turpis. '
                       'Curabitur quam leo, interdum et urna eget, blandit finibus diam. '
                       'Sed ex nunc, tincidunt eu justo a, tempus lobortis felis. '
                       'Mauris maximus augue massa. '
                       'Etiam tristique ligula turpis, id facilisis turpis mattis sit amet. '
                       'Etiam vehicula mauris in lacus tincidunt, quis convallis ipsum condimentum. '
                       'Nam facilisis porta dui at consectetur. '
                       'Etiam eget dui nulla. Proin ac consequat nulla. '
                       'Cras vel nisi nec purus pretium commodo sit amet sed ex. '
                       'Nulla facilisi.\n'
                       '\n'
                       'Sed et est sit amet dui bibendum vulputate id vel enim. '
                       'Nam pharetra blandit metus. '
                       'Aenean aliquam et eros tempus posuere. '
                       'Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
                       'Quisque vitae ullamcorper enim. '
                       'Maecenas neque ex, facilisis vel arcu quis, varius posuere est. '
                       'Proin blandit, justo quis convallis lacinia, odio libero tincidunt velit, '
                       'rhoncus gravida tortor mauris id sapien. '
                       'Cras non ex purus. '
                       'Sed pharetra turpis sit amet elit placerat tincidunt.\n'
                       '\n'
                       'https://vk.com/durov?z=photo1_376599151%2Falbum1_0%2Frev\n'
                       'https://vk.com/durov?z=album1_136592355\n'
                       'https://vk.com/durov?z=video1708231_171383594%2Fvideos1%2Fpl_1_-2\n'
                       'https://www.youtube.com/watch?v=AaIf4X_wgA8&index=9&list=LLUf7lCSmCzdlbjiyLRwH4ww\n'
                       'https://vimeo.com/13525706\n'
                       'https://vk.com/kevinspacey?z=album198977223_180522826\n'
                       'https://www.youtube.com/watch?v=kYfNvmF0Bqw\n'
                       'https://vk.com/durov?z=photo11316927_428929212%2Fwall1_1237616\n'
                       'https://pp.vk.me/c7003/v7003978/1ed9/yoeGXOWmW-M.jpg\n'
                       'https://vk.com/durov?z=photo1_326652857%2Fphotos1'
                   ),
                   attachments=[{'photo': VKPhoto(owner_id=198977223, object_id=342951381, album_id=-6, album='profile',
                                                  date_time=datetime.datetime(2014, 11, 3, 1, 22, 18), user_id=None,
                                                  text=None,
                                                  link='http://cs620320.vk.me/v620320223/1dfe8/KdfGcqsZ3Cc.jpg')}],
                   date_time=datetime.datetime(2016, 10, 17, 3, 54, 45), likes_count=0, reposts_count=0,
                   comments_count=0),
            VKPost(
                owner_id=-129836227, object_id=2, from_id=-129836227, created_by=0,
                text=(
                    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
                     'Nulla sit amet leo magna. '
                     'Etiam convallis metus in mollis ultrices. '
                     'In purus velit, vehicula ut turpis sit amet, faucibus mollis nibh. '
                     'Duis dolor tellus, malesuada eget pellentesque et, pellentesque sed ante. '
                     'Ut tincidunt lacus et vulputate commodo. '
                     'Fusce eu nunc semper, vulputate eros commodo, lacinia diam. '
                     'Vestibulum semper justo at nisl tempus pellentesque. '
                     'Proin sed ultrices elit, eu viverra metus. '
                     'Vestibulum bibendum ornare finibus. '
                     'Fusce luctus in metus et fermentum. '
                     'Aenean non tortor risus.'
                ),
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
