from gomer.counter import counter
import abc
import enum
import json
import logging
from gomer.exceptions import MessageNotRespond, MessageExecuteFail


class ContentCode(enum.Enum):
    MOVE = 1101  # open-loop control
    MOVE_DIRECTLY = 1102  # closed-loop control
    TURN = 1103  # closed-loop control
    FOREARM_OPEN = 1111  # open-loop control
    FOREARM_CLOSE = 1112  # closed-loop control
    ARM_OPEN = 1121  # open-loop control
    ARM_CLOSE = 1122  # closed-loop control
    HEAD_OPEN = 1131  # open-loop control
    HEAD_CLOSE = 1132  # closed-loop control
    PAW_OPEN = 1141  # open-loop control
    PAW_CLOSE = 1142  # closed-loop control
    TTS = 1201
    PLAY_NOTES = 1202
    VOLUME = 1204
    PLAY_STATUS = 1205
    PLAY_FILE = 1206
    STOP_PLAY = 1207
    SET_LIGHT_COLOR = 1001
    LIGHT_SWITCH = 1002
    SET_LIGHT_MODE = 1003
    CLIFF_DETECT = 1011
    INFRARED = 1021
    GYROSCOPE = 1031
    DETECT_FACE = 3101
    GET_FACE_FEATURE = 3102
    REGISTER_FACE = 3103
    GET_NAME = 3104
    GET_EXPRESSION = 3105
    GET_FEATURE_FILE = 3106
    GET_SIMILARITY = 3107
    RENAME = 3108
    GET_FACE_LIST = 3109
    DELETE_FACE = 3110
    DETECT_PATTERN = 3201
    ADD_PATTERN = 3202
    DEL_PATTERN = 3203
    RENAME_PATTERN = 3204
    GET_PATTERN_LIST = 3205
    GET_PATTERN_LOCATION = 3206
    MOVE_TO_PATTERN = 3211
    SHOW_IMAGE = 1301
    SHOW_CAMERA = 1303
    GET_SHOW_STATUS = 1302
    STOP_SHOWING = 1304
    PLAY_EMOTION = 1401
    EMOTION_STATUS = 1402
    PLAY_CUSTOM_EMOTION = 1403
    STOP_EMOTION = 1404


class Message(metaclass=abc.ABCMeta):

    def __init__(self, content, sequence=None):
        self.logger = logging.getLogger('gomer.message')
        self.sequence = sequence
        self.content = content
        self.key = None
        self.message_type = None
        self.code = None

        self.responsed = False
        self.interrupted = False
        self.completed = False

    def __str__(self):
        if self.code:
            message = {"seq": self.sequence, "msgtype": self.message_type, "code": self.code}
        else:
            message = {"seq": self.sequence, "msgtype": self.message_type, self.key: self.content.to_dict()}
        return json.dumps(message)

    def is_response(self):
        if self.message_type == MessageType.RESPONSE.value:
            return True
        return False

    def is_interrupted(self, message):
        if message.sequence > self.sequence:
            self.interrupted = True
        return self.interrupted

    def is_complete(self):
        if self.message_type == MessageType.REQUEST.value:
            return True
        return False

    @classmethod
    def from_dict(cls, message):
        key = (message.keys() & MessageKey._value2member_map_.keys()).pop()
        _cls = cls(content=Content.from_dict(message[key]), sequence=message.get('seq'))
        _cls.key = key
        _cls.message_type = message.get('msgtype')
        _cls.code = message.get('code')
        return _cls


class BlockStatus(enum.Enum):
    NEVER = 'never'
    AUTO = 'auto'
    ALL = 'all'


class MessageType(enum.Enum):
    NORMAL = 0
    REQUEST = 1
    RESPONSE = 2


class MessageKey(enum.Enum):
    HARD = 'hard'  # for hardware: id version wifi language volume battery
    TRANSMIT = 'transmit'  # for file transmission and
    CONTROL = 'control'  # switches for video mode and upgrade
    GROWTH = 'growth'
    MOTOR = 'motor'
    DATABASE = 'database'
    SDKS = 'sdks'  # for Python SDK


class ResultCode(enum.Enum):
    SUCCESS = 100
    FAIL = 101


class RequestMessage(Message):
    def __init__(self, content, sequence=None):
        super().__init__(content, sequence)
        self.message_type = MessageType.REQUEST.value


class ResponseMessage(Message):
    def __init__(self, content, sequence=None):
        super().__init__(content, sequence)
        self.message_type = MessageType.RESPONSE.value


class SDKRequestMessage(RequestMessage):
    def __init__(self, content, block, sequence=None, group=None):
        super().__init__(content, sequence)
        self.key = MessageKey.SDKS.value
        self.sequence = counter.get_sequence()
        self.group = group
        self.block = block
        self.complete_message = None

    def check_response(self, message):
        if self.content.num == message.content.num:
            if message.code == ResultCode.SUCCESS.value:
                self.responsed = True
            else:
                self.logger.error('Message not respond.')
                raise MessageNotRespond('Message not respond.')
        return self.responsed

    def check_complete(self, message):
        if self.content.num == message.content.num:
            if message.content.result == ResultCode.SUCCESS.value:
                self.completed = True
                self.complete_message = message
            else:
                self.logger.error('Message execute fail.')
                raise MessageExecuteFail(
                    'Message execute fail.message is {},complete message is: {}'.format(self, message))
        return self.completed


class SDKResponseMessage(RequestMessage):
    def __init__(self, content, sequence=None):
        super().__init__(content, sequence)
        self.key = MessageKey.SDKS.value


class Content(object):
    def __init__(self, item, num=None, prm1=None, prm2=None, prm3=None, prm4=None, prm5=None, prmstr1=None,
                 prmstr2=None, prmstr3=None, prmstr4=None, prmstr5=None, result=None):
        self.num = num if num else counter.generate_sequence()
        self.item = item
        self.prm1 = prm1
        self.prm2 = prm2
        self.prm3 = prm3
        self.prm4 = prm4
        self.prm5 = prm5
        self.prmstr1 = prmstr1
        self.prmstr2 = prmstr2
        self.prmstr3 = prmstr3
        self.prmstr4 = prmstr4
        self.prmstr5 = prmstr5
        self.result = result

    def to_dict(self):
        content = {}
        for k, v in self.__dict__.items():
            if v is not None:
                content[k] = v
        return content

    @classmethod
    def from_dict(cls, content):
        return cls(item=content.get('item'), num=content.get('num'), prm1=content.get('prm1'), prm2=content.get('prm2'),
                   prm3=content.get('prm3'), prm4=content.get('prm4'), prm5=content.get('prm5'),
                   prmstr1=content.get('prmstr1'), prmstr2=content.get('prmstr2'), prmstr3=content.get('prmstr3'),
                   prmstr4=content.get('prmstr4'), prmstr5=content.get('prmstr5'), result=content.get('result'))
