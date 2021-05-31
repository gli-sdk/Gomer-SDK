import configparser
import threading
import os
from gomer import home
import logging


class Config(object):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Config, '_instance'):
            with Config._instance_lock:
                if not hasattr(Config, '_instance'):
                    Config._instance = object.__new__(cls)
        return Config._instance

    def __init__(self):
        # get config.ini path
        path = self.__get_path()
        self.config = configparser.ConfigParser()
        self.config.read(path, encoding='utf-8')
        self.logger = logging.getLogger('gomer.config')

    def get_glproto(self):
        return os.path.join(home, self.config.get('glproto', 'path'))

    # get file path of config.ini

    def __get_path(self):
        path = os.path.join(home, 'conf/config.ini')
        if not os.path.isfile(path):
            self.logger.error('Can\'t find conf/config.ini, please check the source code.')
            raise FileNotFoundError
        return path



