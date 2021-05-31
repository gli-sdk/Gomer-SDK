import logging
from gomer.base_function import BaseFunction
from gomer.message import ContentCode, Content, SDKRequestMessage
from gomer.exceptions import InvalidParameter
import json


class FaceDetection(BaseFunction):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('gomer.face_detection')
        self.show = True
        self.show_code = 101
        self.face_num = 0
        self.faces = self.__get_face_list()
        self.MAX_LEN = 10

    def show_face(self):
        self.show = True
        self.show_code = 101

    def close_face(self):
        self.show = False
        self.show_code = 100

    def detect_face(self, min_size, max_size):
        try:
            assert isinstance(min_size, int) and 10 <= min_size <= 300
            assert isinstance(max_size, int) and 10 <= max_size <= 300
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
        content = Content(item=ContentCode.DETECT_FACE.value, prm1=source, prm2=min_size, prm3=max_size, prm4=0,
                          prm5=self.show_code)
        message = SDKRequestMessage(content=content, block='all', group=None)
        result = self.sender.send(message)
        face_list = result.get('prmstr1'), result.get('prmstr2'), result.get('prmstr3'), result.get(
            'prmstr4'), result.get('prmstr5')
        faces = [list((json.loads(x).values()))[0][:4] for x in face_list if x is not None]
        self.face_num = len(faces)
        self.logger.info("Gomer has detected {} faces.".format(self.face_num))
        return faces

    def __check_index(self, index):
        if self.face_num == 0:
            self.logger.info('You have not detect face yet.')
            return None
        try:
            assert isinstance(index, int) and 0 <= index <= self.face_num - 1
        except AssertionError as e:
            raise InvalidParameter(
                'Invalid parameter, please check your params, 0 <= index <= {}.'.format(self.face_num - 1))
        return 'face{}'.format(index)

    def get_face_feature(self, index):
        index = self.__check_index(index)
        content = Content(item=ContentCode.GET_FACE_FEATURE.value, prm5=self.show_code, prmstr1=index)
        message = SDKRequestMessage(content=content, block='all', group=None)
        result = self.sender.send(message)
        result = result.get('prmstr1')
        if result:
            result = list(json.loads(result).values())[0]
            return [[result[2 * n], result[2 * n + 1]] for n in range(len(result) // 2)]
        return None

    def get_name(self, index):
        index = self.__check_index(index)

        content = Content(item=ContentCode.GET_NAME.value, prm5=self.show_code, prmstr1=index)
        message = SDKRequestMessage(content=content, block='all', group=None)
        result = self.sender.send(message)
        return result.get('prmstr1')

    # not implemented
    def get_expression(self, index):
        index = 'face{}'.format(index)
        content = Content(item=ContentCode.GET_EXPRESSION.value, prm5=self.show_code, prmstr1=index)
        message = SDKRequestMessage(content=content, block='all', group=None)
        result = self.sender.send(message)
        return result.get('prm1')

    def register_face(self, index, name):
        index = self.__check_index(index)
        try:
            assert isinstance(name, str) and len(name) <= 10
        except AssertionError as e:
            raise InvalidParameter(
                'Invalid parameter, please check your params, name is str and len(name) <= 10.')
        if name in self.faces:
            self.faces.remove(name)
            self.delete_face(name)
        elif len(self.faces) == self.MAX_LEN:
            self.delete_face(self.faces[0])
            self.faces = self.faces[1:]
        self.faces.append(name)
        content = Content(item=ContentCode.REGISTER_FACE.value, prmstr1=index, prmstr2=name)
        message = SDKRequestMessage(content=content, block='all', group=None)
        self.sender.send(message)

    def set_face_feature_file(self, index, filename):
        index = self.__check_index(index)
        try:
            assert isinstance(filename, str) and len(filename) <= 10
        except AssertionError as e:
            raise InvalidParameter("Invalid parameter, len(filename) <= 10.")

        content = Content(item=ContentCode.GET_FEATURE_FILE.value, prmstr1=index, prmstr2=filename)
        message = SDKRequestMessage(content=content, block='all', group=None)
        self.sender.send(message)

    def get_similarity(self, face_file1, face_file2):
        content = Content(item=ContentCode.GET_SIMILARITY.value, prmstr1=face_file1, prmstr2=face_file2)
        message = SDKRequestMessage(content=content, block='all', group=None)
        result = self.sender.send(message)
        result = result.get('prm1')
        return result

    def rename(self, name, new_name):
        try:
            assert isinstance(new_name, str) and len(new_name) <= 10
        except AssertionError as e:
            raise InvalidParameter(
                'Invalid parameter, please check your params, '
                'new_name is str and len(new_name) <= 10.')
        content = Content(item=ContentCode.RENAME.value, prmstr1=name, prmstr2=new_name)
        message = SDKRequestMessage(content=content, block='all', group=None)
        self.sender.send(message)

    def __get_face_list(self):
        faces = []
        content = Content(item=ContentCode.GET_FACE_LIST.value)
        message = SDKRequestMessage(content=content, block='all', group=None)
        result = self.sender.send(message)
        result = result.get('prmstr1')
        if result:
            faces = list(json.loads(result).values())[0]
        return faces

    def get_face_list(self):
        return self.faces

    def delete_face(self, name):
        try:
            assert isinstance(name, str) and name in self.faces
        except AssertionError as e:
            raise InvalidParameter(
                'name does not exists in Gomer! You can check names in Gomer using get_face_list() function.')
        content = Content(item=ContentCode.DETECT_FACE.value, prmstr1=name)
        message = SDKRequestMessage(content=content, block='all', group=None)
        self.sender.send(message)
