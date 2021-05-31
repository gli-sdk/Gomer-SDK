import logging
from .message import ContentCode, Content, SDKRequestMessage
from .base_function import BaseFunction
from .exceptions import InvalidParameter


class Emotion(BaseFunction):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('gomer.emotion')
        self.group = 'emotion'
        self.expression_switch = 101
        self.voice_switch = 101
        self.motion_switch = 101
        self.emotion_set = (
            'a_apl', 'agy_a', 'b_blk', 'c_cat', 'cat_a', 'dbt_a', 'dizy', 'dns_a', 'dog_a', 'hi_a', 'hi_b', 'hll_a',
            'hpy_a', 'hpy_b', 'hpy_sl', 'hpy_swl', 'hrt_a', 'nap_a', 'nap_b', 'obt_a', 'obt_b', 'obt_c', 'scr_a',
            'scr_b', 'sd_a', 'sd_e', 'sgh_a', 'shy_a', 'slp_a', 'snz_a', 'sok_a', 'sok_wt', 'st_a', 'td_a', 'wgl_a',
            'ywn_a', 'ywn_b', 'hry', 'ntsy', 'song_a', 'song_b', 'song_c')

    def turn_on_expression(self):
        self.expression_switch = 101

    def turn_off_expression(self):
        self.expression_switch = 100

    def turn_on_voice(self):
        self.voice_switch = 101

    def turn_off_voice(self):
        self.voice_switch = 100

    def turn_on_motion(self):
        self.motion_switch = 101

    def turn_off_motion(self):
        self.motion_switch = 100

    def stop(self):
        content = Content(ContentCode.STOP_EMOTION.value)
        message = SDKRequestMessage(content=content, block='all')
        self.sender.send(message)

    def play_emotion(self, emotion):
        try:
            assert isinstance(emotion, str) and emotion in self.emotion_set
        except AssertionError as e:
            raise InvalidParameter(
                'Invalid parameter, please check your params, emotion should be in {}'.format(self.emotion_set))
        content = Content(ContentCode.PLAY_EMOTION.value, prm1=self.expression_switch, prm2=self.voice_switch,
                          prm3=self.motion_switch, prmstr1=emotion)
        message = SDKRequestMessage(
            content=content, block='auto', group=self.group)
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
        content = Content(ContentCode.SHOW_CAMERA.value)
        message = SDKRequestMessage(content=content, block='never')
        self.sender.send(message)
