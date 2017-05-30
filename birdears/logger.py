"""
This submodule exports `logger` to log events.

Logging messages which are less severe than `lvl` will be ignored

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
"""

import logging

from logging.config import dictConfig

logging.getLogger(__name__).addHandler(logging.NullHandler())
logging_config = dict(
    version = 1,
    formatters = {
        'f': {
            'format':
              # '%(asctime)s %(module)s %(levelname)-8s\n%(message)s',
              '%(module)s %(levelname)-8s\n%(message)s',
              # '%(asctime)s %(name)-12s %(module)s \
              # %(levelname)-8s %(message)s',
             'datefmt': '%Y/%m/%d,%H:%M:%S',
        }
    },
    handlers = {
        'h': {
                'class': 'logging.StreamHandler',
                'formatter': 'f',
                'level': logging.DEBUG,
        }
    },
    root = {
        'handlers': ['h'],
        'level': logging.DEBUG,
    },
)

dictConfig(logging_config)

logger = logging.getLogger()
