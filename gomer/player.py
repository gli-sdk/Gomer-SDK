import logging
from .message import ContentCode, Content, SDKRequestMessage
from .base_function import *


class Player(BaseFunction):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('gomer.player')
        self.group = 'player'

    def tts(self, string, filename):
        try:
            assert isinstance(string, str) and len(string) < 100
            assert isinstance(filename, str) and len(filename) < 10
        except AssertionError as e:
            raise InvalidParameter(
                'Invalid parameter, please check your params, string is str and len(string) < 100,'
                ' filename is str, and len(filename) < 10')
        content = Content(ContentCode.TTS.value,
                          prmstr1=string, prmstr2=filename)
        message = SDKRequestMessage(content=content, block='all')
        self.sender.send(message)

    # not implemented now
    def play_notes(self, notes, filename, speed):
        '''This function is not avaiable now'''
        content = Content(ContentCode.PLAY_NOTES.value,
                          prm2=speed, prmstr1=notes, prmstr2=filename)
        message = SDKRequestMessage(content=content, block='never')
        self.sender.send(message)

    def set_volume(self, volume):
        try:
            assert isinstance(volume, int) and 1 <= volume <= 5
        except AssertionError as e:
            raise InvalidParameter(
                'Invalid parameter, please check your params, 1 <= volume <= 5')
        content = Content(ContentCode.VOLUME.value, prm1=101, prm2=volume)
        message = SDKRequestMessage(content=content, block='all')
        self.sender.send(message)

    # result message is always 1
    def get_volume(self):
        content = Content(ContentCode.VOLUME.value, prm1=102)
        message = SDKRequestMessage(content=content, block='all')
        result = self.sender.send(message)
        return result.get('prm2')

    def play_file(self, filename):
        content = Content(ContentCode.PLAY_FILE.value, prmstr1=filename)
        message = SDKRequestMessage(
            content=content, block='auto', group=self.group)
        self.sender.send(message)

    def stop(self):
        content = Content(ContentCode.STOP_PLAY.value)
        message = SDKRequestMessage(content=content, block='all')
        self.sender.send(message)

    def get_play_status(self):
        content = Content(ContentCode.PLAY_STATUS.value)
        message = SDKRequestMessage(content=content, block='all')
        result = self.sender.send(message)
        if result.get('prm1') == 100:
            return False
        else:
            return True
