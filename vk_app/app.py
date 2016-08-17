import json

from vk import API, Session, AuthSession

from vk_app.config import VK_SCRIPT_GET_ALL


class App:
    def __init__(self, app_id: str, user_login: str, user_password: str, scope: str, access_token='',
                 api_version='5.53'):
        """Creates instance of our application for working with VK API.
        You have to specify authentication data for app (`app_id`) and user (`user_login`, `user_password`, `scope`)
         or `access_token` parameter.

        :param app_id: your VK application identifier

        full list of your VK applications available at https://new.vk.com/apps?act=manage
        :param user_login: email address or telephone number
        :param user_password:
        :param scope: required permissions separated by colons
        for example: "photos,audio" will give access to user's photos and audio files

        more info at https://new.vk.com/dev/permissions

        :param access_token: special access key which needed to run most of VK API methods

        more info at https://vk.com/dev/access_token
        :param api_version: version of using VK API

        more info at https://vk.com/dev/versions
        """
        if access_token:
            self.session = Session(access_token)
        else:
            self.app_id = app_id
            self.user_login = user_login
            self.user_password = user_password
            self.scope = scope
            self.session = AuthSession(**self.__dict__)
        self.api_version = api_version
        self.api_session = API(self.session, v=self.api_version)

    def __repr__(self):
        return "VK application with id '{}' authorized by user '{}'".format(self.user_login, self.app_id)

    def get_items(self, method: str, params: dict):
        """Get VK countable objects (wall posts, audios, photo albums, photos, videos, etc.)

        :param method: name of API method. Ex.: 'photos.get'

        for the full list check https://new.vk.com/dev/methods
        :param params: method's parameters. Ex. for method 'photos.get':
        {owner_id: 11283070, album_id: 'saved', offset: 300, count: 1000}
        to get saved photos from 300 to 1300 of user with id 11283070 in chronological order

        more info about `method_name` parameters at https://new.vk.com/dev/`method_name`
        :type params: dict
        :return:
        """
        params['count'] = 100

        key = 'items'
        offset = 0
        items = []
        while True:
            params['offset'] = offset
            params_json = json.dumps(params)
            code = VK_SCRIPT_GET_ALL.format(method, key, params_json)
            code_res = self.api_session.execute(code=code)
            items += code_res[key]
            offset = code_res['offset']
            count = code_res['count']
            if offset >= count:
                return items
