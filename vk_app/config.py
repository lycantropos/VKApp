import logging.config
import os

VK_SCRIPT_GET_ALL = """var params = {2};
var max_count = params.count, init_offset = params.offset, key = "{1}", offset_count = init_offset;
var vk_api_req = API.{0}(params), c = vk_api_req.count, items_count = vk_api_req[key], i = 1;

while (i < 25 && offset_count + max_count <= c) {{
    offset_count = i * max_count + init_offset;
    params.offset = offset_count;
    items_count = items_count + API.{0}(params)[key];
    i = i + 1;
}}

return {{count: c, items: items_count, offset: offset_count + max_count, max_c: max_count}};
"""


class LoggingConfig:
    def __init__(self, base_dir: str, logging_config_path: str, logs_path: str):
        self.base_dir = base_dir
        self.logging_config_path = logging_config_path
        self.logs_path = logs_path

    def set(self):
        self.check_logs_dir()
        self.set_log_config_file_path()

    def check_logs_dir(self):
        logs_dir = os.path.dirname(self.logs_path)
        abs_logs_dir = os.path.join(self.base_dir, logs_dir)
        if not os.path.exists(abs_logs_dir):
            os.makedirs(abs_logs_dir)

    def set_log_config_file_path(self):
        log_config_full_path = os.path.join(self.base_dir, self.logging_config_path)
        logging.config.fileConfig(log_config_full_path, defaults={'logfilename': self.logs_path})
