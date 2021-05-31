import logging
from gomer.base_function import *
import enum
import os
from gomer.exceptions import InvalidFileType
import cv2 as cv
import numpy as np


class FileType(enum.Enum):
    SaveVoice = 101
    SaveImage = 102
    PlayWithoutSaveVoice = 201
    NotSaveImage = 202
    NotSaveAndNotPlayVoice = 204


class UploadResult(enum.Enum):
    WrongType = -1
    WrongPath = -2
    FileIsNone = -3
    UploadBusy = -4
    UploadError = -5
    OK = 1


class Uploader(BaseFunction):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('gomer.uploader')
        self.image_types = ('jpg', 'jpeg', 'bmp', 'png')
        self.voice_types = ('mp3', 'wav')

    def upload(self, path):
        width = 320
        height = 180
        new_path = path.replace('/', '\\')
        if not os.path.exists(path):
            raise FileNotFoundError('{} not found.'.format(path))
        filename = path.split('\\')[-1]
        suffix = filename.split('.')[-1]
        upload_path = os.path.join(os.path.dirname(path), 'gomer_upload')
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        if suffix in self.voice_types:
            self.sender.upload(
                file_type=FileType.SaveVoice.value, path=new_path)
        elif suffix in self.image_types:
            image = cv.imread(new_path)
            img_height, img_width = image.shape[:2]
            bg = np.zeros([height, width, 3], np.uint8)
            if img_width / img_height < width / height:
                n_width = img_width * height // img_height // 2 * 2
                n_img = cv.resize(
                    image, (n_width, height))
                bg[:, (width - n_width) // 2:(width + n_width) // 2] = n_img
            elif img_width / img_height > width / height:
                n_height = img_height * width // img_height // 2 * 2
                n_img = cv.resize(image, (width, n_height))
                bg[(height - n_height) // 2:(height + n_height) // 2, :] = n_img
            else:
                bg = cv.resize(image, (width, height))
            filename = filename - suffix + 'jpg'
            u_path = os.path.join(upload_path, filename)
            cv.imwrite(u_path, bg)
            self.sender.upload(file_type=FileType.SaveImage.value, path=u_path)
        else:
            raise InvalidFileType('Please check your file type, it should be in {} or {}'.format(
                self.image_types, self.voice_types))
