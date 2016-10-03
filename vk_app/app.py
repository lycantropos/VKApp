import json

from vk import API, Session, AuthSession


class App:
    def __init__(self, app_id: int = 0, user_login: str = '', user_password: str = '', scope: str = '',
                 access_token: str = '', api_version: str = '5.56'):
        """Creates instance of our application for working with VK API.
        You have to specify authentication data for app (`app_id`) and user (`user_login`, `user_password`, `scope`)
         or `access_token` parameter.

        :param app_id: your VK application identifier

        full list of your VK applications available at https://vk.com/apps?act=manage
        :param user_login: email address or telephone number
        :param user_password:
        :param scope: required permissions separated by colons
        for example: "photos,audio" will give access to user's photos and audio files

        more info at https://vk.com/dev/permissions

        :param access_token: special access key which needed to run most of VK API methods

        more info at https://vk.com/dev/access_token
        :param api_version: version of using VK API

        more info at https://vk.com/dev/versions
        """
        if access_token:
            self.session = Session(access_token)
            self.access_token = access_token
        else:
            self.app_id = app_id
            self.user_login = user_login
            self.user_password = user_password
            self.scope = scope
            self.session = AuthSession(**self.__dict__)
            self.access_token = self.session.access_token
        self.api_version = api_version
        self.api_session = API(self.session, v=self.api_version)

    def get_items(self, method: str, params: dict):
        """Get VK countable objects (wall posts, audios, photo albums, photos, videos, etc.)

        :param method: name of API method. Ex.: 'photos.get'

        for the full list check https://new.vk.com/dev/methods
        :param params: method's parameters. Ex. for method 'photos.get':
        {owner_id: 11283070, album_id: 'saved', offset: 300, count: 1000}
        to get saved photos from 300 to 1300 of user with id 11283070 in chronological order

        more info about `method_name` parameters at https://vk.com/dev/`method_name`
        :type params: dict
        :return:
        """
        params['count'] = 100

        key = 'items'
        offset = params.get('offset', 0)
        items = []
        while True:
            params['offset'] = offset
            params_json = json.dumps(params)
            code = VK_SCRIPT_GET_ALL.format(method=method, key=key, params=params_json)
            code_res = self.api_session.execute(code=code)
            items += code_res[key]
            offset = code_res['offset']
            if offset >= code_res['count']:
                return items


VK_SCRIPT_GET_ALL = """var params = {params};
var max_count = params.count, init_offset = params.offset, key = "{key}", offset_count = init_offset;
var vk_api_req = API.{method}(params), c = vk_api_req.count, items_count = vk_api_req[key], i = 1;

while (i < 25 && offset_count + max_count <= c) {{
    offset_count = i * max_count + init_offset;
    params.offset = offset_count;
    items_count = items_count + API.{method}(params)[key];
    i = i + 1;
}}

return {{count: c, items: items_count, offset: offset_count + max_count, max_c: max_count}};
"""
