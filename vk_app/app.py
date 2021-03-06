import json
import os
from functools import wraps
from typing import List, Tuple, Callable, Any

import requests
from vk_app.services import download
from vk_app.utils import solve_captcha
from vk import API, Session, AuthSession
from vk.exceptions import VkAPIError


def captchured(captcha_img_path: str = os.path.join(os.path.expanduser('~'), 'captcha.png'),
               captcha_solver: Callable[[str], str] = solve_captcha):
    """
    Decorator with parameters for taking care of
    sending too frequent requests to VK API
    with possibility of entering CAPTCHA text

    :param captcha_img_path: file path for CAPTCHA image to be stored at,
    user's home directory by default
    :param captcha_solver: function which receives path to CAPTCHA image and returns CAPTCHA text
    :return: decorator
    """

    def resolve_captcha(function: Callable[[Any], Any]):
        """
        :param function: function which sends requests to VK API
        and may require CAPTCHA in cases of frequent requests
        :return: function with ability of resolving CAPTCHA
        """

        @wraps(function)
        def resolved_captcha(*args, **kwargs):
            """
            Runs function in infinite loop
            until correct text CAPTCHA entered

            :param args: positional function arguments
            :param kwargs: keyword function arguments
            :return: result of wrapped function or runs forever
            """
            while True:
                try:
                    return function(*args, **kwargs)
                except VkAPIError as error:
                    if error.code == error.CAPTCHA_NEEDED:
                        download(error.captcha_img, captcha_img_path)
                        captcha_key = captcha_solver(captcha_img_path)
                        os.remove(captcha_img_path)
                        kwargs['captcha_sid'] = error.captcha_sid
                        kwargs['captcha_key'] = captcha_key
                    else:
                        raise error

        return resolved_captcha

    return resolve_captcha


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

    def __repr__(self):
        return 'App:<app_id={self.app_id}, ' \
               'user_login={self.user_login}, ' \
               'api_version={self.api_version}>'.format(self=self)

    def get_all_objects(self, method: str, **params):
        """Returns all VK countable objects (wall posts, audios, photo albums, photos, videos, etc.)

        :param method: name of API method. Ex.: 'photos.get'

        for the full list check https://new.vk.com/dev/methods
        :param params: method's parameters. Ex. for method 'photos.get':
        {owner_id: 11283070, album_id: 'saved', offset: 300, count: 1000}
        to get saved photos from 300 to 1300 of user with id 11283070 in chronological order

        more info about `method_name` parameters at https://vk.com/dev/`method_name`
        :return:
        """
        params['count'] = 100
        params.setdefault('offset', 0)

        key = 'items'
        items = list()
        while True:
            params_json = json.dumps(params)
            code = VK_SCRIPT_GET_ALL.format(method=method, key=key, params=params_json)
            code_res = self.api_session.execute(code=code, **params)
            items += code_res[key]
            params['offset'] = code_res['offset']
            if len(items) >= code_res['count']:
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

        return self.api_session.__call__(method, **params)


VK_SCRIPT_GET_ALL = """var params = {params};
var count = params.count, offset = params.offset, key = "{key}";
var res = API.{method}(params);
var total_count = res.count, items = res[key], api_calls = 1;

while (api_calls < 25 && params.offset + count <= total_count) {{
    params.offset = params.offset + count;
    items = items + API.{method}(params)[key];
    api_calls = api_calls + 1;
}}

return {{"count": total_count, "items": items, "offset": params.offset}};
"""
