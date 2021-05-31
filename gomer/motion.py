from .message import SDKRequestMessage, Content, ContentCode
from .base_function import *
import logging


class Motion(BaseFunction):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('gomer.motion')


class Wheel(Motion):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('gomer.wheel')
        self.group = 'wheel'

    '''open-loop control for wheels of Gomer
        block style: auto never all
    '''

    def move(self, speed, timeout, block):
        try:
            assert isinstance(speed, int) and -2 <= speed <= 2 and speed != 0
            assert isinstance(timeout, int) and 0 <= timeout <= 10000
            assert isinstance(block, str) and block in self.block_mode_set
        except AssertionError as e:
            raise InvalidParameter(
                'Invalid parameter, please check input parameters. -3 <= speed <= 3 and speed != 0,'
                ' 0 <= timeout <= 10000, block in {}.'.format(self.block_mode_set))
        angle = 0
        if speed < 0:
            speed = - speed
            angle = 180
        content = Content(item=ContentCode.MOVE.value,
                          prm1=speed, prm2=angle, prm3=timeout)
        message = SDKRequestMessage(
            content=content, block=block, group=self.group)
        self.sender.send(message)

    def move_directly(self, speed, distance, timeout, block):
        try:
            assert isinstance(speed, int) and 1 <= speed <= 3
            assert isinstance(distance, int) and -1000 <= distance <= 1000
            assert isinstance(timeout, int) and 0 <= timeout <= 10000
            assert isinstance(block, str) and block in self.block_mode_set
        except AssertionError as e:
            raise InvalidParameter(
                'Invalid parameter, please check input parameters. 1 <= speed <= 3, -1000 <= distance <= 1000, '
                '0 <= timeout <= 10000, block in {}.'.format(self.block_mode_set))

        content = Content(item=ContentCode.MOVE_DIRECTLY.value,
                          prm1=speed, prm2=distance, prm3=timeout)
        message = SDKRequestMessage(
            content=content, block=block, group=self.group)
        self.sender.send(message)

    def turn(self, speed, angle, timeout, block):
        try:
            assert isinstance(speed, int) and 1 <= speed <= 3
            assert isinstance(angle, int) and -360 <= angle <= 360
            assert isinstance(timeout, int) and 0 <= timeout <= 10000
            assert isinstance(block, str) and block in self.block_mode_set
        except AssertionError as e:
            raise InvalidParameter(
                'Invalid parameter, please check input parameters. 1 <= speed <= 3,'
                ' -360 <= angle <= 360, 0 <= timeout <= 10000, block in {}.'.format(self.block_mode_set))

        content = Content(item=ContentCode.TURN.value,
                          prm1=speed, prm2=angle, prm3=timeout)
        message = SDKRequestMessage(
            content=content, block=block, group=self.group)
        self.sender.send(message)


class Forearm(Motion):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('gomer.forearm')

        self.group = 'forearm'

    def open_loop_move(self, speed, timeout, block):
        try:
            assert isinstance(speed, int) and -2 <= speed <= 2 and speed != 0
            assert isinstance(timeout, int) and 0 <= timeout <= 10000
            assert isinstance(block, str) and block in self.block_mode_set
        except AssertionError as e:
            raise InvalidParameter(
                'Invalid parameter, please check input parameters. -3 <= speed <= 3 not 0,'
                ' 0 <= timeout <= 10000, block in {}.'.format(self.block_mode_set))
        content = Content(item=ContentCode.FOREARM_OPEN.value,
                          prm1=speed, prm3=timeout)
        message = SDKRequestMessage(
            content=content, block=block, group=self.group)
        self.sender.send(message)

    def closed_loop_move(self, speed, angle, timeout, block):
        try:
            assert isinstance(speed, int) and 1 <= speed <= 3
            assert isinstance(angle, int) and 0 <= angle <= 210
            assert isinstance(timeout, int) and 0 <= timeout <= 10000
            assert isinstance(block, str) and block in self.block_mode_set
        except AssertionError as e:
            raise InvalidParameter(
                'Invalid parameter, please check input parameters. 1 <= speed <= 3,'
                ' 0 <= angle <= 210, 0 <= timeout <= 10000, block in {}.'.format(self.block_mode_set))
        content = Content(item=ContentCode.FOREARM_CLOSE.value,
                          prm1=speed, prm2=angle, prm3=timeout)
        message = SDKRequestMessage(
            content=content, block=block, group=self.group)
        self.sender.send(message)


class Arm(Motion):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('gomer.arm')

        self.group = 'arm'

    def open_loop_move(self, speed, timeout, block):
        try:
            assert isinstance(speed, int) and -2 <= speed <= 2 and speed != 0
            assert isinstance(timeout, int) and 0 <= timeout <= 10000
            assert isinstance(block, str) and block in self.block_mode_set
        except AssertionError as e:
            raise InvalidParameter(
                'Invalid parameter, please check input parameters. -3 <= speed <= 3 not 0,'
                ' 0 <= timeout <= 10000, block in {}.'.format(self.block_mode_set))
        content = Content(item=ContentCode.ARM_OPEN.value,
                          prm1=speed, prm3=timeout)
        message = SDKRequestMessage(
            content=content, block=block, group=self.group)
        self.sender.send(message)

    def closed_loop_move(self, speed, angle, timeout, block):
        try:
            assert isinstance(speed, int) and 1 <= speed <= 3
            assert isinstance(angle, int) and 0 <= angle <= 160
            assert isinstance(timeout, int) and 0 <= timeout <= 10000
            assert isinstance(block, str) and block in self.block_mode_set
        except AssertionError as e:
            raise InvalidParameter(
                'Invalid parameter, please check input parameters. 1 <= speed <= 3,'
                ' 0 <= angle <= 160, 0 <= timeout <= 10000, block in {}.'.format(self.block_mode_set))
        content = Content(item=ContentCode.ARM_CLOSE.value,
                          prm1=speed, prm2=angle, prm3=timeout)
        message = SDKRequestMessage(
            content=content, block=block, group=self.group)
        self.sender.send(message)


class Head(Motion):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('gomer.head')
        self.group = 'head'

    def open_loop_move(self, speed, timeout, block):
        try:
            assert isinstance(speed, int) and -2 <= speed <= 2 and speed != 0
            assert isinstance(timeout, int) and 0 <= timeout <= 10000
            assert isinstance(block, str) and block in self.block_mode_set
        except AssertionError as e:
            raise InvalidParameter(
                'Invalid parameter, please check input parameters. -3 <= speed <= 3 not 0,'
                ' 0 <= timeout <= 10000, block in {}.'.format(self.block_mode_set))
        content = Content(item=ContentCode.HEAD_OPEN.value,
                          prm1=speed, prm3=timeout)
        message = SDKRequestMessage(
            content=content, block=block, group=self.group)
        self.sender.send(message)

    def closed_loop_move(self, speed, angle, timeout, block):
        try:
            assert isinstance(speed, int) and 1 <= speed <= 3
            assert isinstance(angle, int) and -15 <= angle <= 65
            assert isinstance(timeout, int) and 0 <= timeout <= 10000
            assert isinstance(block, str) and block in self.block_mode_set
        except AssertionError as e:
            raise InvalidParameter(
                'Invalid parameter, please check input parameters. 1 <= speed <= 3,'
                '-15 <= angle <= 65, 0 <= timeout <= 10000, block in {}.'.format(self.block_mode_set))
        content = Content(item=ContentCode.HEAD_CLOSE.value,
                          prm1=speed, prm2=angle, prm3=timeout)
        message = SDKRequestMessage(
            content=content, block=block, group=self.group)
        self.sender.send(message)


class Paw(Motion):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('gomer.paw')

        self.group = 'paw'

    def open_loop_move(self, speed, timeout, block):
        try:
            assert isinstance(speed, int) and -2 <= speed <= 2 and speed != 0
            assert isinstance(timeout, int) and 0 <= timeout <= 10000
            assert isinstance(block, str) and block in self.block_mode_set
        except AssertionError as e:
            raise InvalidParameter(
                'Invalid parameter, please check input parameters. -3 <= speed <= 3 not 0,'
                ' 0 <= timeout <= 10000, block in {}.'.format(self.block_mode_set))
        content = Content(item=ContentCode.PAW_OPEN.value,
                          prm1=speed, prm3=timeout)
        message = SDKRequestMessage(
            content=content, block=block, group=self.group)
        self.sender.send(message)

    def closed_loop_move(self, speed, angle, timeout, block):
        try:
            assert isinstance(speed, int) and 1 <= speed <= 3
            assert isinstance(angle, int) and 0 <= angle <= 100
            assert isinstance(timeout, int) and 0 <= timeout <= 10000
            assert isinstance(block, str) and block in self.block_mode_set
        except AssertionError as e:
            raise InvalidParameter(
                'Invalid parameter, please check input parameters. 1 <= speed <= 3,'
                '0 <= angle <= 100, 0 <= timeout <= 10000, block in {}.'.format(self.block_mode_set))
        content = Content(item=ContentCode.PAW_CLOSE.value,
                          prm1=speed, prm2=angle, prm3=timeout)
        message = SDKRequestMessage(
            content=content, block=block, group=self.group)
        self.sender.send(message)
