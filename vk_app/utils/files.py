import os
from urllib.request import urlopen


def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None


def check_dir(folder_path: str, *subfolders):
    full_path = os.path.join(folder_path, *subfolders)
    if not os.path.exists(full_path):
        os.mkdir(full_path)


def get_valid_folders(*folders) -> list:
    valid_folders = filter(None, folders)
    valid_folders = list(valid_folders)
    return valid_folders


def download(link: str, save_path: str):
    if not os.path.exists(save_path):
        response = urlopen(link)
        if response.status == 200:
            with open(save_path, 'wb') as out:
                image_content = response.read()
                out.write(image_content)
