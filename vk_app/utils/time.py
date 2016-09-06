import threading
from datetime import datetime

# hyphen was chosen because its MySQL default DATE separator
DATE_SEP = '-'
DATE_ORDER = ['%Y', '%m', '%d']
DATE_FORMAT = DATE_SEP.join(DATE_ORDER)


def make_periodic(delay: int):
    """Decorator with parameter for making functions periodically launched
    :param delay: period in which function should be called, in seconds
    :return: periodic function
    """

    def launch_periodically(function):
        def launched_periodically(*args, **kwargs):
            timer = threading.Timer(delay, function, args=args, kwargs=kwargs)
            try:
                timer.start()
            except RuntimeError:
                timer.cancel()
                launched_periodically(*args, **kwargs)

        return launched_periodically

    return launch_periodically


def get_date_from_millis(millis: int) -> str:
    date = datetime.fromtimestamp(millis).strftime(DATE_FORMAT)
    return date


def get_year_month_date(date: str, sep='.') -> str:
    year_month_date = sep.join(date.split(DATE_SEP)[:-1])
    return year_month_date
