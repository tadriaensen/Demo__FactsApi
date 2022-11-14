__author__ = 'Tom Adriaensen'
__maintainer__ = 'Tom Adriaensen'
__status__ = 'Production'
__version__ = '1.0.0'

import time
import datetime as dt
import random


def wait(seconds_to_wait: int, print_message_to_console: bool = False, log_level: str = None, log_component: str = None):
    """
    Function to perform a wait during code execution.
    The number of seconds provided is the number of seconds the code execution will pause.
    If a number, lower than 1 is provided, the wait time is 1 second
    """
    if seconds_to_wait <= 1:
        seconds_to_wait = 1

    if print_message_to_console:
        message = 'Wait {seconds_to_wait} seconds, to continue execution'.format(seconds_to_wait=seconds_to_wait)
        if log_component is None:
            log_entry = '{timestamp} -- {log_level} -- {message}'.format(timestamp=dt.datetime.now().now().strftime('%Y-%m-%d %H:%M:%S'),
                                                                         log_level=log_level.upper(),
                                                                         message=message
                                                                         )
        else:
            log_entry = '{timestamp} -- {log_level} -- {log_component} -- {message}'.format(timestamp=dt.datetime.now().now().strftime('%Y-%m-%d %H:%M:%S'),
                                                                                            log_level=log_level.upper(),
                                                                                            log_component=log_component,
                                                                                            message=message
                                                                                            )
        print(log_entry)

    time.sleep(seconds_to_wait)


def variable_wait(max_seconds_to_wait: int, print_message_to_console: bool = False, log_level: str = None, log_component: str = None):
    """
    Function to perform a wait during code execution.
    The number of seconds provided is the max number of seconds the code execution will pause.
    If a number, lower than 1 is provided, the wait time is 1 second
    """
    if max_seconds_to_wait <= 1:
        seconds_to_wait = 1
    else:
        seconds_to_wait = random.randint(1, max_seconds_to_wait)

    if print_message_to_console:
        message = 'Wait {seconds_to_wait} seconds, to continue execution'.format(seconds_to_wait=seconds_to_wait)
        if log_component is None:
            log_entry = '{timestamp} -- {log_level} -- {message}'.format(timestamp=dt.datetime.now().now().strftime('%Y-%m-%d %H:%M:%S'),
                                                                         log_level=log_level.upper(),
                                                                         message=message
                                                                         )
        else:
            log_entry = '{timestamp} -- {log_level} -- {log_component} -- {message}'.format(timestamp=dt.datetime.now().now().strftime('%Y-%m-%d %H:%M:%S'),
                                                                                            log_level=log_level.upper(),
                                                                                            log_component=log_component,
                                                                                            message=message
                                                                                            )
        print(log_entry)

    time.sleep(seconds_to_wait)
