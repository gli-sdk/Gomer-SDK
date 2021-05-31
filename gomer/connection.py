from ctypes import *
from .config import Config
from .exceptions import NoDevicesFound
import logging
import threading
from queue import Queue
import time


class Connection:
    _instance_lock = threading.Lock()
    message_queue = Queue()
    yuvs = Queue()

    @CFUNCTYPE(c_int, POINTER(c_ubyte), c_int, c_int)
    def receive_video_data(yuv_file, width, height):
        yuv = string_at(yuv_file, int(width * height * 3 / 2))
        Connection.yuvs.put_nowait(yuv)
        return 0

    @CFUNCTYPE(c_int, c_char_p, c_int)
    def receive(message, len):
        Connection.message_queue.put(message)
        return 0

    @CFUNCTYPE(c_int, c_int)
    def receive_upload_result(self, result):
        return 0

    def __new__(cls, *args, **kwargs):
        if not hasattr(Connection, '_instance'):
            with Connection._instance_lock:
                if not hasattr(Connection, '_instance'):
                    Connection._instance = object.__new__(cls)
        return Connection._instance

    def __init__(self):
        self.logger = logging.getLogger('gomer.connection')
        self.__lib = CDLL(Config().get_glproto())

    def __search(self):
        num = c_int()
        devices = (c_char_p * 5)()
        res = self.__lib.ProtocolSearchDevice(byref(num), devices)

        if res != 1:
            self.logger.error('Can\'n find a gomer in wifi.')
            raise NoDevicesFound('No gomer can be found, please check wifi connection of your PC!')

    def connect(self, name):
        self.__search()
        name_p = c_char_p(name.encode())

        res = self.__lib.ProtocolConnectDevice(name_p, self.receive)
        if res == 1:
            self.logger.info('Connect {} success...'.format(name))
            print('connect success')
        # waiting for ready
        time.sleep(4)

    # destroy connection with Gomer
    def destroy(self):
        res = self.__lib.ProtocolDestroyConnect()
        if res == 0:
            self.__lib = None
            return

    def send(self, message):
        message_p = create_string_buffer(message.encode())
        self.__lib.ProtocolSendMessage(message_p)

    def upload(self, file_type, path):
        path_p = c_char_p(path.encode())

        res = self.__lib.ProtocolSendFileBlock(file_type, path_p)
        if res == 1:
            return
        else:
            print('error uploading, error code is {}'.format(res))

    def upload_async(self, file_type, path):
        path_p = c_char_p(path.encode())
        self.__lib.ProtocolSendFileUnblock(file_type, path_p, self.receive_upload_result)

    def open_video_data(self):
        self.__lib.ProtocolOpenVideo(self.receive_video_data)

    def close_video_data(self):
        self.__lib.ProtocolCloseVideo()

    def open_video(self):
        self.__lib.ProtocolOpenVideoAndDisplay()

    def close_video(self):
        res = self.__lib.ProtocolCloseVideoAndDisplay()
        if res == 0:
            return
