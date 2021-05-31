from gomer.base_function import *
import cv2 as cv
import numpy as np
import threading


class Video(BaseFunction):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('gomer.video')
        self.open = False
        self.yuv = None

    def open_video(self):
        self.sender.open_video()

    def close_video(self):
        self.sender.close_video()

    def open_video_data(self, yuv_queue):
        self.sender.open_video_data()
        self.open = True
        video_thread = threading.Thread(target=self.handle_video_data, args=(yuv_queue,))
        video_thread.setDaemon(True)
        video_thread.start()

    def handle_video_data(self, yuv_queue):
        while self.open:
            if not yuv_queue.empty():
                self.yuv = yuv_queue.get()

    def get_image(self):
        height = 720
        width = 1280
        yuv = self.yuv
        image_array = np.frombuffer(yuv, np.uint8)
        yuv = np.reshape(image_array, (int(height * 3 / 2), int(width)))
        new_img = cv.cvtColor(yuv, cv.COLOR_YUV2BGR_I420)
        return new_img

    def close_video_data(self):
        self.open = False
        self.sender.close_video_data()
