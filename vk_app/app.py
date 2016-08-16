import json

from vk import API, AuthSession

from vk_app.config import VK_SCRIPT_GET_ALL


class App:
    def __init__(self, app_id: str, user_login: str, user_password: str, scope: str, api_version='5.52'):
        """Creates instance of our application for working with VK API

        :param app_id: your VK application identifier

        full list of your VK applications available at https://new.vk.com/apps?act=manage
        :param user_login: email or telephone number
        :param user_password:
        :param scope: required permissions separated by colons
        for example: "photos,audio" will give access to user's photos and audio files

        more info at https://new.vk.com/dev/permissions
        :param api_version:
        """
        self.app_id = app_id
        self.user_login = user_login
        self.user_password = user_password
        self.scope = scope
        self.auth_session = AuthSession(**self.__dict__)
        self.api_version = api_version
        self.api_session = API(self.auth_session, v=self.api_version)

    def __repr__(self):
        return "VK application with id '{}' authorized by user '{}'".format(self.user_login, self.app_id)

    def get_items(self, method: str, params: dict, key='items'):
        """Get VK countable objects (wall posts, audios, photo albums, photos, videos)

        :param method: name of API method. Ex.: 'photos.get'

        for the full list check https://new.vk.com/dev/methods
        :type method: str
        :param params: method's parameters. Ex. for method 'photos.get':
        {owner_id: 11283070, album_id: 'saved', offset: 300, count: 1000}
        to get saved photos from 300 to 1300 of user with id 11283070 in chronological order

        more info about `method_name` parameters at https://new.vk.com/dev/`method_name`
        :type params: dict
        :param key:
        :type key: str
        :return:
        :rtype: list
        """
        params['count'] = 100

        offset = 0
        res = []
        while True:
            params['offset'] = offset
            params_json = json.dumps(params)
            code = VK_SCRIPT_GET_ALL.format(method, key, params_json)
            code_res = self.api_session.execute(code=code)
            res += code_res[key]
            offset = code_res['offset']
            if offset >= code_res['count']:
                return res
