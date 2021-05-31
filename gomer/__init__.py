import logging.handlers
import logging
__all__ = [
    '__version__',
    'base_function',
    'config',
    'counter',
    'exceptions',
    'message',
    'motion',
    'robot'
]

import os
from gomer.__version__ import *
import sys
import platform

# check python version
if sys.version_info < (3, 7, 4) or platform.architecture()[0] != '64bit':
    raise Exception(
        'Please check your python version. A x64 Python above v3.7.4 is needed.')
# get home path of gomer
home = os.path.abspath(os.path.dirname(__file__))
root = os.path.dirname(home)


def get_logger(home):
    datefmt = '%Y-%m-%d %H:%M:%S'
    logger = logging.getLogger("gomer")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s %(filename)s[line: %(lineno)d] %(levelname)s: %(message)s')
    formatter.datefmt = datefmt
    logger_dir = os.path.join(home, 'logs')
    if not os.path.exists(logger_dir):
        os.makedirs(logger_dir)

    logger_path = os.path.join(logger_dir, 'mylog.log')
    if not os.path.exists(logger_path):
        file = open(logger_path, 'w')
        file.close()

    print(logger_path)

    file_handler = logging.handlers.RotatingFileHandler(
        logger_path, 'ab', 1 * 1024 * 1024, 3)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.NOTSET)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


logger = get_logger(home)

logger.info("*****Welcome to the world of Gomer. Just enjoy it!*****")
logger.info("SDK version: {}, Gomer version required: >= {}.{}.{}, Update time: {}, Copyright: {}"
            .format(VERSION, MINIMUM_GOMER_VERSION[0], MINIMUM_GOMER_VERSION[1], MINIMUM_GOMER_VERSION[2], UPDATE_TIME,
                    COPYRIGHT))
