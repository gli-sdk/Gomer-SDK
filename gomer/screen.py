import logging
from .message import ContentCode, Content, SDKRequestMessage
from .base_function import BaseFunction


class Screen(BaseFunction):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('gomer.screen')
        self.group = 'screen'

    def stop_showing(self):
        content = Content(ContentCode.STOP_SHOWING.value)
        message = SDKRequestMessage(content=content, block='all')
        self.sender.send(message)

    def show_image(self, image):
        content = Content(ContentCode.SHOW_IMAGE.value, prm1=1000, prmstr1=image)
        message = SDKRequestMessage(content=content, block='never')
        self.sender.send(message)

    def is_showing(self):
        content = Content(ContentCode.GET_SHOW_STATUS.value)
        message = SDKRequestMessage(content=content, block='all')
        result = self.sender.send(message)
        result = result.get('prm1')
        if result == 101:
            return True
        else:
            return False

    def show_camera(self):
        content = Content(ContentCode.SHOW_CAMERA.value, prm1=101)
        message = SDKRequestMessage(content=content, block='all')
        self.sender.send(message)


