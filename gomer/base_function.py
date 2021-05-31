import logging
from .transceiver import MessageSender


class BaseFunction(object):
    def __init__(self):
        self.logger = logging.getLogger('gomer.base_function')
        self.sender = MessageSender()
        self.block_mode_set = ('auto', 'never', 'all')
