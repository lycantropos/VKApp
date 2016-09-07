import logging.config
import os


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
        abs_log_config_path = os.path.join(self.base_dir, self.logging_config_path)
        abs_logs_path = os.path.join(self.base_dir, self.logs_path)
        logging.config.fileConfig(abs_log_config_path, defaults={'logfilename': abs_logs_path})
