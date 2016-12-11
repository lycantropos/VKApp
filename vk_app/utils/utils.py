import datetime
import inspect
import logging
import logging.config
import os
import re
import threading
import time
from collections import OrderedDict
from functools import wraps
from typing import Callable, List, Any

from PIL import Image
from sqlalchemy import (Boolean, Column, DateTime, Integer,
                        LargeBinary, String, Interval, Time)

__all__ = ['make_periodic', 'make_delayed', 'get_year_month_date',
           'get_normalized_file_name', 'find_file',
           'set_logging_config', 'solve_captcha', 'check_dir',
           'get_valid_dirs', 'map_non_primary_columns_by_ancestor',
           'get_all_subclasses', 'get_repr', 'obj_to_dict']

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
        names_parameters = ancestor_initializer_signature.parameters
        non_self_parameters = list(names_parameters.values())[1:]
        for parameter in non_self_parameters:
            if parameter.annotation in PYTHON_SQLALCHEMY_TYPES:
                setattr(
                    inheritor, parameter.name,
                    Column(
                        PYTHON_SQLALCHEMY_TYPES[parameter.annotation],
                        nullable=parameter.default is None
                    )
                )
            else:
                logging.warning(
                    'There is no appropriate SQLAlchemy type found for `{}`'
                    .format(parameter.annotation.__name__)
                )
    else:
        raise NotImplementedError('It is available to map columns '
                                  'by class\'s initializer '
                                  'only for its children')


AnyFunction = Callable[..., Any]
VoidFunction = Callable[..., None]


def make_periodic(period_in_sec: float) -> Callable[[VoidFunction], VoidFunction]:
    """Decorator with parameter for making functions periodically launched"""

    if period_in_sec <= 0.:
        raise ValueError('Non-positive period: {}'.format(period_in_sec))

    class CallRepeater:
        def __init__(self):
            self.call_event = threading.Event()
            self.last_call_time = time.time()

        def launch_periodically(self, function: VoidFunction) -> VoidFunction:
            @wraps(function)
            def launched_periodically(*args, **kwargs):
                while not self.call_event.wait(self.last_call_time - time.time()):
                    function(*args, **kwargs)
                    self.last_call_time += period_in_sec
                    logging.debug(
                        'Next call of `{}` will be at {}'.format(
                            function.__name__,
                            datetime.datetime.fromtimestamp(self.last_call_time)
                            .isoformat(' ')
                        )
                    )

            return launched_periodically

    call_repeater = CallRepeater()

    return call_repeater.launch_periodically


def make_delayed(delay_in_seconds: float) -> Callable[[AnyFunction], AnyFunction]:
    """Decorator with parameter for making functions launched with minimal delay between calls"""

    if delay_in_seconds <= 0.:
        raise ValueError('Non-positive delay: {}'.format(delay_in_seconds))

    class CallDelayer:
        def __init__(self):
            self.call_event = threading.Event()
            self.last_call_time = time.time()

        def launch_with_delay(self, function: AnyFunction) -> AnyFunction:
            @wraps(function)
            def launched_with_delay(*args, **kwargs):
                self.last_call_time += delay_in_seconds
                res = function(*args, **kwargs)
                wait_sec = self.last_call_time - time.time()
                logging.debug(
                    'Next call of `{}` will be available at {}'.format(
                        function.__name__,
                        datetime.datetime.fromtimestamp(self.last_call_time).isoformat(' ')
                    )
                )
                self.call_event.wait(wait_sec)
                return res

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


def set_logging_config(base_dir: str, logging_config_path: str, logs_path: str,
                       disable_existing_loggers=True):
    logs_dir = os.path.dirname(logs_path)
    check_dir(base_dir, logs_dir, create=True)
    abs_log_config_path = os.path.join(base_dir, logging_config_path)
    abs_logs_path = os.path.join(base_dir, logs_path)
    logging.config.fileConfig(fname=abs_log_config_path,
                              defaults={'logfilename': abs_logs_path},
                              disable_existing_loggers=disable_existing_loggers)


def get_normalized_file_name(name: str, ext: str):
    return name[:MAX_FILE_NAME_LEN - len(ext)].replace(os.sep, ' ') + ext


def check_dir(root: str, *subs, create=False):
    if not os.path.exists(root):
        if create:
            os.mkdir(root)
        else:
            err_message = 'Directory {} does not exist.'.format(root)
            raise ValueError(err_message)

    path = root
    for sub in subs:
        path = os.path.join(path, sub)
        if not os.path.exists(path):
            if create:
                os.mkdir(path)
            else:
                err_message = 'Directory {} does not exist.'.format(root)
                raise ValueError(err_message)


def get_valid_dirs(*dirs) -> List[str]:
    valid_dirs = filter(None, dirs)
    valid_dirs = list(valid_dirs)
    return valid_dirs


CAPTCHA_RE = re.compile('\w+', re.UNICODE)


def solve_captcha(path: str):
    show_captcha(path)
    while True:
        captcha_key = input('Please enter the captcha key '
                            'from image located at {}:\n'
                            .format(path))
        if not CAPTCHA_RE.match(captcha_key):
            logging.info('Incorrect captcha format, repeat input.')
        else:
            break


def show_captcha(path: str):
    with Image.open(path) as img:
        size = tuple([4 * x for x in img.size])
        img = img.resize(size)
        img.show(path)


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
    initializer_signature = inspect.signature(cls.__init__)
    arguments = OrderedDict(initializer_signature.parameters)
    arguments.pop('self')
    cls_repr = '{cls_name}({{}})'.format(cls_name=cls.__name__)
    # '!r' flag forces to get `repr()` of object
    init_signature = ', '.join('{argument}={{{argument}!r}}'.format(argument=argument)
                               for argument in arguments)
    cls_repr = cls_repr.format(init_signature)
    return cls_repr


def obj_to_dict(obj) -> dict:
    initializer_signature = inspect.signature(obj.__init__)
    arguments = OrderedDict(initializer_signature.parameters)
    obj_dict = dict(
        (argument, getattr(obj, argument))
        for argument in arguments
    )
    return obj_dict
