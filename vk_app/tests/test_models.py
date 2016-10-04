import unittest
from datetime import datetime, time

from models.attachments import VKPhoto, VKAudio, VKVideo, VKDoc, VKNote, VKPoll
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
            owner_id=1, object_id=278184324, user_id=0, album_id=-6, album='profile',
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
            player_link='https://vk.com/video_ext.php?oid=33151248&id=170594858&hash=6af70b680de137f8&__ref='
                        'vk.api&api_hash=1475515983cb93631fcefce81573_GMZTCNJRGI2DQ',
            link='https://cs543305.vk.me/u234346085/videos/29dfb3e3d8.720.mp4?extra='
                 'XngTjD0nYtvFXmjf7xzcujLkgw5kNUlXTL1xTjbToBnKF2J_Qaj'
                 '-ZzFC_XXWAid_-6qSn1iW75kysTYVN-cz53p52MDo_nFar-n64fK4wVTPr1_qeiIz8ZE3h9ME6TlApGtGpNYhcA',
            adding_date=datetime(2014, 11, 4, 3, 9, 22)
        )

        self.raw_poll = dict(
            id=81690974,
            owner_id=2314852,
            created=1364338248,
            question='Question',
            votes=208,
            answer_id=0,
            answers=[
                dict(
                    id=259181111,
                    text='Option 1',
                    votes=187,
                    rate=89.9
                ),
                dict(
                    id=259181112,
                    text='Option 2',
                    votes=11,
                    rate=5.29
                ),
                dict(
                    id=259181113,
                    text='Option 3',
                    votes=10,
                    rate=4.81
                )
            ],
            anonymous=1
        )
        self.poll = VKPoll(
            owner_id=2314852, object_id=81690974, question='Question',
            answers=[
                dict(
                    id=259181111,
                    text='Option 1',
                    votes=187,
                    rate=89.9
                ),
                dict(
                    id=259181112,
                    text='Option 2',
                    votes=11,
                    rate=5.29
                ),
                dict(
                    id=259181113,
                    text='Option 3',
                    votes=10,
                    rate=4.81
                )
            ],
            anonymous=True, date_time=datetime(2013, 3, 27, 5, 50, 48), votes_count=208
        )

        self.raw_post = dict(
            id=3000, from_id=33151248, owner_id=33151248, date=1475513354, post_type="post", text="&#128567;",
            can_edit=1, can_delete=1, can_pin=1,
            attachments=[
                dict(
                    type="photo",
                    photo=dict(
                        id=435501272, album_id=-23,
                        owner_id=33151248,
                        photo_75="https://pp.vk.me/c636223/v636223248/34934/R_hAK8m0JD0.jpg",
                        photo_130="https://pp.vk.me/c636223/v636223248/34935/KM9H5qIU9zc.jpg",
                        photo_604="https://pp.vk.me/c636223/v636223248/34936/gTSsz726TIo.jpg",
                        photo_807="https://pp.vk.me/c636223/v636223248/34937/LEFha8J80BM.jpg",
                        photo_1280="https://pp.vk.me/c636223/v636223248/34938/t1lKrWNWWro.jpg",
                        width=1176, height=588, text="", date=1475513276, access_key="853346876714b6fc16"
                    )
                ),
                dict(
                    type="video",
                    video=dict(
                        id=171222918, owner_id=239068454, title="Арабская ночь", duration=57, description="",
                        date=1422221463, views=179954, comments=211,
                        photo_130="https://pp.vk.me/c543504/u239068454/video/s_58f5159c.jpg",
                        photo_320="https://pp.vk.me/c543504/u239068454/video/l_648bbca6.jpg",
                        photo_800="https://pp.vk.me/c543504/u239068454/video/x_364dac38.jpg",
                        access_key="175761fb2d96ea9e3a", repeat=1, can_add=1
                    )
                ),
                dict(
                    type="photo",
                    photo=dict(
                        id=430441958, album_id=235405921, owner_id=33151248,
                        photo_75="https://pp.vk.me/c630731/v630731248/4fc77/08Yn_3H7sh0.jpg",
                        photo_130="https://pp.vk.me/c630731/v630731248/4fc78/CjmjCnjc_jc.jpg",
                        photo_604="https://pp.vk.me/c630731/v630731248/4fc79/MvmFFvwhn8k.jpg",
                        photo_807="https://pp.vk.me/c630731/v630731248/4fc7a/aD8ZIlnkwT0.jpg",
                        photo_1280="https://pp.vk.me/c630731/v630731248/4fc7b/Ha--FXqt3KE.jpg",
                        photo_2560="https://pp.vk.me/c630731/v630731248/4fc7c/SxOzgVokHx8.jpg",
                        width=2560, height=1707, text="", date=1472545544, access_key="40c37e8eeaa37e4dbf"
                    )
                ),
                dict(
                    type="doc",
                    doc=dict(
                        id=437638505, owner_id=33151248, title="o-SEB-facebook.jpg", size=309626, ext="jpg",
                        url="https://psv4.vk.me/c810332/u33151248/docs/568f49ec97c6/o-SEB-facebook.jpg?extra="
                            "TRh7RRKRBMR13_rCM7QeM2Avn9ydUzIWel9j_26ONar-dTEtbai1wfMog5_"
                            "mmrB7zTH0HwsWfJAC1xMVioqOyLwd6WP-7y4yz4vGkuMGIFdmg8jB99iGwVtr",
                        date=1467224041, type=4,
                        preview=dict(
                            photo=dict(
                                sizes=[
                                    dict(
                                        src="https://pp.vk.me/c812736/u132472508/-3/m_c2b672ecec.jpg",
                                        width=130, height=78, type="m"
                                    ),
                                    dict(
                                        src="https://pp.vk.me/c812736/u132472508/-3/s_c2b672ecec.jpg",
                                        width=100, height=60, type="s"
                                    ),
                                    dict(
                                        src="https://pp.vk.me/c812736/u132472508/-3/x_c2b672ecec.jpg",
                                        width=604, height=360, type="x"
                                    ),
                                    dict(
                                        src="https://pp.vk.me/c812736/u132472508/-3/y_c2b672ecec.jpg",
                                        width=807, height=481, type="y"
                                    ),
                                    dict(
                                        src="https://pp.vk.me/c812736/u132472508/-3/z_c2b672ecec.jpg",
                                        width=1280, height=762, type="z"
                                    ),
                                    dict(
                                        src="https://pp.vk.me/c812736/u132472508/-3/o_c2b672ecec.jpg",
                                        width=1536, height=914, type="o"
                                    )
                                ]
                            )
                        ),
                        access_key="a9c64e3c4e37c82cfa")),
                dict(
                    type="audio",
                    audio=dict(
                        id=456239374, owner_id=2000012511, artist="Ludovico Einaudi", title="In un'altra vita",
                        duration=595, date=1475513340,
                        url="https://cs4-3v4.vk-cdn.net/p24/c94608ff7b7048.mp3?extra=uQMvvJy9sTqWFU1DTxk90_"
                            "g1sNbh47Uc01CMII0_CbD1BBhAYydqe9dB7OkWOUNl59m0vrgVJgt7aGJoN8j8VVazs9ZvnvJV5onC9"
                            "a5nhgkjrnv3okPymmp0XBW1gskQB6wOovpKdd-GjqF2",
                        lyrics_id=11400950, album_id=2, genre_id=16
                    )
                ),
                dict(
                    type="poll",
                    poll=dict(
                        id=240277467, owner_id=33151248, created=1475513339, question='test', votes=7, answers=[
                            dict(
                                id=801878765,
                                text='option1',
                                votes=1,
                                rate=14.29
                            ),
                            dict(
                                id=801878766,
                                text='option2',
                                votes=6,
                                rate=85.71
                            )
                        ],
                        answer_id=801878766, anonymous=0
                    )
                ),
                dict(
                    type="note",
                    note=dict(
                        id=11850515, owner_id=33151248, comments=0, read_comments=0, date=1475513236,
                        title="note title",
                        view_url="https://m.vk.com/note33151248_11850515?api_view=1ad8c2cf1beac3d1b58bc211bdf769"
                    )
                )
            ],
            post_source=dict(type="vk"), comments=dict(count=0, can_post=1),
            likes=dict(count=1, user_likes=0, can_like=1, can_publish=0),
            reposts=dict(count=0, user_reposted=0)
        )
        self.post = VKPost(
            owner_id=33151248, object_id=3000, from_id=33151248, created_by=0, comment='&#128567;',
            attachments=dict(
                audio=[
                    VKAudio(
                        owner_id=2000012511, object_id=456239374, artist='Ludovico Einaudi',
                        title="In un'altra vita", duration=time(0, 9, 55), date_time=datetime(2016, 10, 3, 23, 49, 0),
                        genre_id=16, lyrics_id=11400950,
                        link='https://cs4-3v4.vk-cdn.net/p24/c94608ff7b7048.mp3?extra='
                             'uQMvvJy9sTqWFU1DTxk90_g1sNbh47Uc01CMII0_CbD1BBhAYydqe9dB7OkWOUNl59m0'
                             'vrgVJgt7aGJoN8j8VVazs9ZvnvJV5onC9a5nhgkjrnv3okPymmp0XBW1gskQB6wOovpKdd-GjqF2'
                    )
                ],
                doc=[
                    VKDoc(
                        owner_id=33151248, object_id=437638505, title='o-SEB-facebook.jpg', size=309626, ext='jpg',
                        link='https://psv4.vk.me/c810332/u33151248/docs/568f49ec97c6/o-SEB-facebook.jpg?extra='
                             'TRh7RRKRBMR13_rCM7QeM2Avn9ydUzIWel9j_26ONar-'
                             'dTEtbai1wfMog5_mmrB7zTH0HwsWfJAC1xMVioqOyLwd6WP-7y4yz4vGkuMGIFdmg8jB99iGwVtr'
                    )
                ],
                note=[
                    VKNote(
                        owner_id=33151248, object_id=11850515, title='note title', text=None,
                        date_time=datetime(2016, 10, 3, 23, 47, 16), comments_count=0
                    )
                ],
                poll=[
                    VKPoll(
                        owner_id=33151248, object_id=240277467, question='test',
                        answers=[
                            {'rate': 14.29, 'text': 'option1', 'id': 801878765, 'votes': 1},
                            {'rate': 85.71, 'text': 'option2', 'id': 801878766, 'votes': 6}
                        ],
                        anonymous=False, date_time=datetime(2016, 10, 3, 23, 48, 59), votes_count=7
                    )
                ],
                photo=[
                    VKPhoto(
                        owner_id=33151248, object_id=435501272, album_id=-23, album='graffiti',
                        date_time=datetime(2016, 10, 3, 23, 47, 56), user_id=None, comment=None,
                        link='https://pp.vk.me/c636223/v636223248/34938/t1lKrWNWWro.jpg'
                    ),
                    VKPhoto(
                        owner_id=33151248, object_id=430441958, album_id=235405921, album=None,
                        date_time=datetime(2016, 8, 30, 15, 25, 44), user_id=None, comment=None,
                        link='https://pp.vk.me/c630731/v630731248/4fc7c/SxOzgVokHx8.jpg'
                    )
                ],
                video=[
                    VKVideo(
                        owner_id=239068454, object_id=171222918, title='Арабская ночь', description=None,
                        duration=time(0, 0, 57), date_time=datetime(2015, 1, 26, 3, 31, 3),
                        views_count=179954, adding_date=None, player_link=None, link=None
                    )
                ]

            ), date_time=datetime(2016, 10, 3, 23, 49, 14), likes_count=1, reposts_count=0, comments_count=0

        )

    def test_vk_photo_from_raw(self):
        photo = VKPhoto.from_raw(self.raw_photo)
        self.assertEqual(photo, self.photo)

    def test_vk_audio_from_raw(self):
        audio = VKAudio.from_raw(self.raw_audio)
        self.assertEqual(audio, self.audio)

    def test_vk_video_from_raw(self):
        video = VKVideo.from_raw(self.raw_video)
        self.assertEqual(video, self.video)

    def test_vk_poll_from_raw(self):
        poll = VKPoll.from_raw(self.raw_poll)
        self.assertEqual(poll, self.poll)

    def test_vk_post_from_raw(self):
        post = VKPost.from_raw(self.raw_post)
        self.assertEqual(post, self.post)
