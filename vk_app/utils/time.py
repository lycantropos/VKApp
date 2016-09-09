import threading
from datetime import datetime


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


def get_year_month_date(date_time: datetime, sep='.') -> str:
    year_month_date = date_time.strftime(sep.join(['%Y', '%m']))
    return year_month_date
