import logging
from gomer.base_function import BaseFunction
from gomer.message import ContentCode, Content, SDKRequestMessage
import json
from gomer.exceptions import InvalidParameter
import re


class PatternDetection(BaseFunction):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('gomer.patter_detection')
        self.show = True
        self.show_code = 101
        self.pattern_group = ('all', 'number', 'letter', 'animal', 'custom')
        self.pattern_num = 0

    def __check_index(self, index):
        if self.pattern_num == 0:
            self.logger.info('You have not detect face yet.')
            return None
        try:
            assert isinstance(index, int) and 0 <= index <= self.pattern_num - 1
        except AssertionError as e:
            raise InvalidParameter(
                'Invalid parameter, please check your params, 0 <= index <= {}.'.format(self.pattern_num - 1))
        return 'pattern{}'.format(index)

    def show(self):
        self.show = True
        self.show_code = 101

    def close(self):
        self.show = False
        self.show_code = 100

    def detect_pattern(self, min_size, max_size, group):
        try:
            assert isinstance(min_size, int) and 10 <= min_size <= 300
            assert isinstance(max_size, int) and 10 <= max_size <= 300
            assert min_size < max_size
            assert isinstance(group, str) and group in self.pattern_group
        except AssertionError as e:
            raise InvalidParameter(
                'Invalid parameter, please check your params, 10 <= min_size <= 300 ,'
                ' 10 <= max_size <= 300.')
        # face image source, this parameter may be exposed in the future.
        # 100 = camera, we use this for default
        # 101 = image data array
        # 102 = image file, when use image file, set prmstr1 as file name.
        source = 100
        # prm4 is min score
        content = Content(item=ContentCode.DETECT_PATTERN.value, prm1=source, prm2=min_size, prm3=max_size, prm4=0,
                          prm5=self.show_code, prmstr2=group)
        message = SDKRequestMessage(content=content, block='all', group=None)
        result = self.sender.send(message)
        pattern_list = result.get('prmstr1'), result.get('prmstr2'), result.get('prmstr3'), result.get(
            'prmstr4'), result.get('prmstr5')
        print(pattern_list)
        patterns = [list(json.loads(x).values())[0][:8] for x in pattern_list if x is not None]

        self.pattern_num = len(patterns)
        return patterns

    def add_pattern(self, pattern_name):
        try:
            assert isinstance(pattern_name, str)
            reg = r'^sdk1_(\d{2})x(\d{2})_\w{1,10}.jpg$'
            groups = re.match(reg, pattern_name)
            assert groups is not None
            assert int(groups.group(1)) == int(groups.group(2))
            assert 30 <= int(groups.group(1)) <= 50
            assert 30 <= int(groups.group(2)) <= 50
        except AssertionError as e:
            raise InvalidParameter(
                'Please check your patter name: sdk1_sizexsize_name.jpg, 30<=size<=50, 1 <=len(name) <= 10.')

        content = Content(item=ContentCode.ADD_PATTERN.value, prmstr1=pattern_name)
        message = SDKRequestMessage(content=content, block='all', group=None)
        self.sender.send(message)

    def get_custom_patterns(self):
        content = Content(item=ContentCode.GET_PATTERN_LIST.value)
        message = SDKRequestMessage(content=content, block='all', group=None)
        result = self.sender.send(message)
        result = result.get('prmstr1')
        if result:
            return json.loads(result).values()
        return None

    def get_pattern_location(self, index):
        index = self.__check_index(index)
        content = Content(item=ContentCode.GET_PATTERN_LOCATION.value, prm5=self.show_code, prmstr1=index)
        message = SDKRequestMessage(content=content, block='all', group=None)
        result = self.sender.send(message)
        result = result.get('prmstr1')
        if result:
            return list(json.loads(result).values())[0]
        return None

    def move_to_pattern(self, pattern, distance):
        content = Content(item=ContentCode.MOVE_TO_PATTERN.value, prm1=distance, prmstr1=pattern)
        message = SDKRequestMessage(content=content, block='all', group=None)
        result = self.sender.send(message)
        if result.get('prm1') == 101:
            return None
        else:
            return result.get('prm2'), result.get('prm3'), result.get('prm4'), result.get('prm5')
