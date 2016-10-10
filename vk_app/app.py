import json
from typing import List, Tuple

import requests
from vk import API, Session, AuthSession


class App:
    def __init__(self, app_id: int = 0, user_login: str = '', user_password: str = '', scope: str = '',
                 access_token: str = '', api_version: str = '5.57'):
        """Initializes instance of our application for working with VK API.
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

    def get_items(self, method: str, **params):
        """Returns VK countable objects (wall posts, audios, photo albums, photos, videos, etc.)

        :param method: name of API method. Ex.: 'photos.get'

        for the full list check https://new.vk.com/dev/methods
        :param params: method's parameters. Ex. for method 'photos.get':
        {owner_id: 11283070, album_id: 'saved', offset: 300, count: 1000}
        to get saved photos from 300 to 1300 of user with id 11283070 in chronological order

        more info about `method_name` parameters at https://vk.com/dev/`method_name`
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

    def get_upload_server_url(self, method: str, **params) -> str:
        """Returns VK server URL for uploading files on it

        :param method: name of API method used to get upload server URL. Ex.: 'photos.getUploadServer'

        for the full list check https://new.vk.com/dev/methods
        :param params: method's parameters. Ex. for method 'photos.getWallUploadServer':
        {}
        to get upload server URL for images to be posted on current user's wall
        :return:
        """
        response = self.api_session.__call__(method, **params)
        upload_url = response['upload_url']
        return upload_url

    def upload_files_on_vk_server(self, method: str, upload_url: str,
                                  files: List[Tuple[str, Tuple[str, bytearray]]], **params) -> List[dict]:
        """Uploads files on VK servers and returns the list of raw VK objects

        :param method: name of API method used to save given by VK IDs objects on user/community page.
        Ex.: `photos.saveOwnerPhoto`.

        for the full list check https://new.vk.com/dev/methods
        :param upload_url: upload server URL which was gotten by `get_upload_server_url` method
        :param files: tuples of 'file' strings with index number postfix and tuples of files' names with its content
        :param params: method's parameters. Ex. for method 'audio.save':
        {}
        to get raw VK audio object with `artist` and `title` fields obtained from ID3 tags
        """
        with requests.Session() as session:
            response = session.post(upload_url, files=files)
            params.update(response.json())

        raw_vk_objects = self.api_session.__call__(method, **params)
        return raw_vk_objects


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
