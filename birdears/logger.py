"""
This submodule exports `logger` to log events.

Logging messages which are less severe than `lvl` will be ignored

```
Level       Numeric value
-----       -------------
CRITICAL    50
ERROR       40
WARNING     30
INFO        20
DEBUG       10
NOTSET      0

Level       When it’s used
-----       --------------
DEBUG       Detailed information, typically of interest only when diagnosing
                problems.
INFO        Confirmation that things are working as expected.
WARNING     An indication that something unexpected happened, or indicative of
                some problem in the near future (e.g. ‘disk space low’).
                The software is still working as expected.
ERROR       Due to a more serious problem, the software has not been able to
                perform some function.
CRITICAL	A serious error, indicating that the program itself may be unable
                to continue running.
```
"""

import logging
from functools import wraps

from logging.config import dictConfig

logging.getLogger(__name__).addHandler(logging.NullHandler())

log_format = """\
%(levelname)s:%(filename)s,%(lineno)s:%(funcName)s() %(message)s\
"""

date_format = '%Y/%m/%d,%H:%M:%S'

logging_config = dict(
    version=1,
    formatters={
        'f': {
             'format': log_format,
             'datefmt': date_format,
        }
    },
    handlers={
        'h': {
                'class': 'logging.StreamHandler',
                'formatter': 'f',
                'level': logging.DEBUG,
        }
    },
    root={
        'handlers': ['h'],
        'level': logging.WARNING,
    },
)

dictConfig(logging_config)

logger = logging.getLogger()


def log_event(f, *args, **kwargs):
    """
    Decorator. Functions and method decorated with this decorator will have
    their signature logged when birdears is executed with `--debug` mode. Both
    function signature with their call values and their return will be logged.
    """

    @wraps(f)
    def decorator(*args, **kwargs):

        # arguments = str(args) # 0 is self
        # kw_arguments = str(kwargs)
        qname = f.__qualname__

        arguments = ', '.join([repr(arg) for arg in args])  # 0 is self
        kw_arguments = ', '.join(['{}={}'.format(k, repr(v))
                                 for k, v in kwargs.items()])

        if logger.isEnabledFor(logging.INFO):
            logger.info("{qname}() called.".format(qname=qname))

        if logger.isEnabledFor(logging.DEBUG):
            # logger.debug("\t*{}, **{}".format(
            # arguments, kw_arguments).expandtabs())
            logger.debug("{qname}({args}, {kwargs})".
                         format(qname=qname, args=arguments,
                                kwargs=kw_arguments). expandtabs())

            # init returns the very own object
            if f.__name__ != '__init__':

                func_return = f(*args, **kwargs)
                logger.debug("{qname} function returned: '{func_ret}'".
                             format(qname=qname, func_ret=func_return))

                return func_return

        return f(*args, **kwargs)

    # RESOLUTION_METHODS.update({f.__name__: f})

    return decorator
