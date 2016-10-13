import datetime
import inspect
import logging
import os
import threading
import time
from collections import OrderedDict
from typing import Callable, List

from sqlalchemy import (Boolean, Column, DateTime, Integer, LargeBinary, String)
from sqlalchemy import Interval
from sqlalchemy import Time

__all__ = ['make_periodic', 'make_delayed', 'get_year_month_date', 'get_normalized_file_name', 'find_file', 'check_dir',
           'get_valid_dirs', 'map_non_primary_columns_by_ancestor', 'get_all_subclasses', 'get_repr']

PYTHON_SQLALCHEMY_TYPES = {
    bool: Boolean,
    bytes: LargeBinary,
    datetime.datetime: DateTime,
    datetime.timedelta: Interval,
    datetime.time: Time,
    int: Integer,
    str: String(255),
}


def map_non_primary_columns_by_ancestor(inheritor: type, ancestor: type):
    if issubclass(inheritor, ancestor):
        ancestor_initializer_signature = inspect.signature(ancestor.__init__)
        arguments = ancestor_initializer_signature.parameters

        for argument in arguments.values():
            if argument.name != 'self':
                if argument.annotation in PYTHON_SQLALCHEMY_TYPES:
                    setattr(
                        inheritor, argument.name,
                        Column(
                            PYTHON_SQLALCHEMY_TYPES[argument.annotation], nullable=argument.default is None
                        )
                    )
                else:
                    logging.warning(
                        "There is no appropriate SQLAlchemy type found for `{}`".format(argument.annotation.__name__))
    else:
        raise NotImplementedError("It is available to map columns by class's initializing only for its children")


VoidFunction = Callable[..., None]


def make_periodic(period_in_sec: float) -> Callable[[VoidFunction], VoidFunction]:
    """Decorator with parameter for making functions periodically launched"""

    if period_in_sec <= 0.:
        raise ValueError("Non-positive period: {}".format(period_in_sec))

    class CallRepeater:
        call_event = threading.Event()
        last_call_time = time.time()

        def launch_periodically(self, function: VoidFunction) -> VoidFunction:
            def launched_periodically(*args, **kwargs):
                while not self.call_event.wait(self.last_call_time - time.time()):
                    function(*args, **kwargs)
                    self.last_call_time += period_in_sec
                    logging.debug(
                        "Next call of `{}` will be at {}".format(
                            function.__name__,
                            datetime.datetime.fromtimestamp(self.last_call_time).isoformat(' ')
                        )
                    )

            return launched_periodically

    call_repeater = CallRepeater()

    return call_repeater.launch_periodically


def make_delayed(delay_in_seconds: float) -> Callable[[VoidFunction], VoidFunction]:
    """Decorator with parameter for making functions launched with minimal delay between calls"""

    if delay_in_seconds <= 0.:
        raise ValueError("Non-positive delay: {}".format(delay_in_seconds))

    class CallDelayer:
        def __init__(self):
            self.call_event = threading.Event()
            self.last_call_time = time.time()

        def launch_with_delay(self, function: VoidFunction) -> VoidFunction:
            def launched_with_delay(*args, **kwargs):
                self.last_call_time += delay_in_seconds
                function(*args, **kwargs)
                wait_sec = self.last_call_time - time.time()
                self.call_event.wait(wait_sec)

            return launched_with_delay

    call_delayer = CallDelayer()
    return call_delayer.launch_with_delay


def get_year_month_date(date_time: datetime.datetime, sep='.') -> str:
    year_month_date_format = sep.join(['%Y', '%m'])
    year_month_date = date_time.strftime(year_month_date_format)
    return year_month_date


def find_file(name: str, path: str) -> str:
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None


MAX_FILE_NAME_LEN = os.pathconf(os.getcwd(), 'PC_NAME_MAX')


def get_normalized_file_name(name: str, ext: str):
    return name[:MAX_FILE_NAME_LEN - len(ext)].replace(os.sep, ' ') + ext


def check_dir(path_dir: str, *subdirs):
    path = path_dir
    if not os.path.exists(path):
        os.mkdir(path)

    for subdir in subdirs:
        path = os.path.join(path, subdir)
        if not os.path.exists(path):
            os.mkdir(path)


def get_valid_dirs(*dirs) -> List[str]:
    valid_dirs = filter(None, dirs)
    valid_dirs = list(valid_dirs)
    return valid_dirs


def get_all_subclasses(cls: type) -> List[type]:
    all_subclasses = cls.__subclasses__() + [
        subsubclass
        for subclass in cls.__subclasses__()
        for subsubclass in get_all_subclasses(subclass)
        ]
    return all_subclasses


def get_repr(instance: object) -> str:
    cls = instance.__class__
    return get_repr_template_by_cls(cls).format(**instance.__dict__)


def get_repr_template_by_cls(cls: type) -> str:
    cls_initializer_signature = inspect.signature(cls.__init__)
    arguments = OrderedDict(cls_initializer_signature.parameters)
    arguments.pop('self')
    cls_repr = "{cls_name}({{}})".format(cls_name=cls.__name__)
    # '!r' flag forces to get `repr()` of object
    init_signature = ', '.join("{argument}={{{argument}!r}}".format(argument=argument) for argument in arguments)
    cls_repr = cls_repr.format(init_signature)
    return cls_repr
