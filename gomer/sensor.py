import logging
from .message import ContentCode, Content, SDKRequestMessage
from .base_function import BaseFunction
import math
from .exceptions import InvalidParameter


class Sensor(BaseFunction):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('gomer.sensor')
        self.group = 'sensor'


    @staticmethod
    def quaternion_to_euler_angles(w, x, y, z):
        roll = math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y)) * 180 / math.pi
        pitch = math.asin(2 * (w * y - z * x)) * 180 / math.pi
        yaw = math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z)) * 180 / math.pi
        return yaw, pitch, roll

    # change rgb to real color
    def set_light_color(self, r, g, b):
        try:
            assert isinstance(r, int) and 0 <= r <= 255
            assert isinstance(g, int) and 0 <= r <= 255
            assert isinstance(b, int) and 0 <= r <= 255
        except AssertionError as e:
            raise InvalidParameter(
                'Invalid parameter, please check your input r,g,b values, they should be in range 0~255.')

        # In gomer rgb ranges in 100, in cv rgb ranges in 255.
        r = int(r / 2.55)
        g = int(g / 2.55)
        b = int(b / 2.55)
        content = Content(item=ContentCode.SET_LIGHT_COLOR.value, prm1=r, prm2=b, prm3=g)
        message = SDKRequestMessage(content=content, block='all')
        self.sender.send(message)

    def light_on(self):
        content = Content(item=ContentCode.LIGHT_SWITCH.value, prm1=101)
        message = SDKRequestMessage(content=content, block='all')
        self.sender.send(message)

    def light_off(self):
        content = Content(item=ContentCode.LIGHT_SWITCH.value, prm1=100)
        message = SDKRequestMessage(content=content, block='all')
        self.sender.send(message)

    def set_light_mode(self, mode, duration, on_time, off_time):
        try:
            assert isinstance(mode, str) and mode in ('on', 'blink', 'breathe')
            assert isinstance(duration, int) and 0 <= duration <= 30000
            assert isinstance(on_time, int) and 0 <= on_time <= 10000
            assert isinstance(off_time, int) and 0 <= off_time <= 10000
        except AssertionError as e:
            raise InvalidParameter(
                'Invalid parameter, please check your input values, mode in ("on", "blink", "breathe"), \
                0 <= duration <= 30000, 0 <= on_time, off_time <= 10000.')

        mode_dict = dict(on=0, blink=1, breathe=2)
        mode = mode_dict.get(mode)
        if on_time == 0:
            on_time = 65535
        content = Content(item=ContentCode.SET_LIGHT_MODE.value, prm1=mode, prm2=duration, prm3=on_time, prm4=off_time)
        message = SDKRequestMessage(content=content, block='all')
        self.sender.send(message)

    def turn_on_cliff_detection(self):
        content = Content(item=ContentCode.CLIFF_DETECT.value, prm1=101)
        message = SDKRequestMessage(content=content, block='all')
        self.sender.send(message)

    def turn_off_cliff_detection(self):
        content = Content(item=ContentCode.CLIFF_DETECT.value, prm1=100)
        message = SDKRequestMessage(content=content, block='all')
        self.sender.send(message)

    def read_infrared(self, location):
        try:
            assert isinstance(location, str) and location in ('front', 'end')
        except AssertionError as e:
            raise InvalidParameter('Invalid parameter, please check your input values, location in ("front", "end")')
        index = dict(front=1, end=2).get(location)
        content = Content(item=ContentCode.INFRARED.value, prm1=index)
        message = SDKRequestMessage(content=content, block='all')
        result = self.sender.send(message)
        return result.get('prm2')

    def read_gyroscope(self):
        content = Content(item=ContentCode.GYROSCOPE.value)
        message = SDKRequestMessage(content=content, block='all')
        result = self.sender.send(message)
        return float(result.get("prm1")) / (1 << 30), float(result.get('prm2')) / (1 << 30), float(
            result.get('prm3')) / (1 << 30), float(result.get('prm4')) / (1 << 30)
