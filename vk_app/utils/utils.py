import logging
import os
import threading
import time
from datetime import datetime
from typing import Callable

__all__ = ['CallRepeater', 'CallDelayer', 'get_year_month_date', 'find_file', 'check_dir', 'get_valid_dirs']

VoidFunction = Callable[..., None]


class CallRepeater:
    call_event = threading.Event()
    last_call_time = time.time()

    @classmethod
    def make_periodic(cls, period_in_sec: float) -> Callable[[VoidFunction], Callable]:
        """Decorator with parameter for making functions periodically launched"""

        if period_in_sec <= 0.:
            raise ValueError("Non-positive period: {}".format(period_in_sec))

        def launch_periodically(function: VoidFunction) -> Callable:
            def launched_periodically(*args, **kwargs):
                while not cls.call_event.wait(cls.last_call_time - time.time()):
                    function(*args, **kwargs)
                    cls.last_call_time += period_in_sec

            return launched_periodically

        return launch_periodically


class CallDelayer:
    call_event = threading.Event()
    last_call_time = time.time()

    @classmethod
    def make_delayed(cls, delay_in_seconds: float) -> Callable[[VoidFunction], Callable]:
        """Decorator with parameter for making functions launched with minimal delay between calls"""

        if delay_in_seconds <= 0.:
            raise ValueError("Non-positive delay: {}".format(delay_in_seconds))

        def launch_with_delay(function: VoidFunction) -> Callable:
            def launched_with_delay(*args, **kwargs):
                cls.last_call_time += delay_in_seconds
                function(*args, **kwargs)
                wait_sec = cls.last_call_time - time.time()
                cls.call_event.wait(wait_sec)

            return launched_with_delay

        return launch_with_delay


def get_year_month_date(date_time: datetime, sep='.') -> str:
    year_month_date_format = sep.join(['%Y', '%m'])
    year_month_date = date_time.strftime(year_month_date_format)
    return year_month_date


def find_file(name: str, path: str):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None


def check_dir(path_dir: str, *subdirs):
    path = path_dir
    if not os.path.exists(path):
        os.mkdir(path)

    for ind, subdir in enumerate(subdirs):
        path = os.path.join(path, subdir)
        if not os.path.exists(path):
            os.mkdir(path)


def get_valid_dirs(*dirs) -> list:
    valid_dirs = filter(None, dirs)
    valid_dirs = list(valid_dirs)
    return valid_dirs
