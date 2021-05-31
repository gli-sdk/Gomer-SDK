import logging
from .message import Message, BlockStatus, ContentCode, MessageType, ResultCode
import time
from .connection import Connection
import threading
from collections import OrderedDict
import json
from .__version__ import MINIMUM_GOMER_VERSION
import re
from .exceptions import GomerNeedsUpdate


class SDKRequestMessageState:
    __shared_dict = {}

    def __init__(self):
        self.__dict__ = self.__shared_dict
        self.block_set = set()
        self.live_messages = OrderedDict()
        # self.results =
        self.logger = logging.getLogger('gomer.message_state')

    def add_item(self, message):
        self.live_messages[message.content.num] = message
        self.add_to_set(message)

    def del_item(self, message):
        self.live_messages.pop(message.content.num)
        if message.block == BlockStatus.NEVER.value or message.block == BlockStatus.ALL.value:
            return
        self.block_set.discard(message.group)

    def add_to_set(self, message):
        if message.block == BlockStatus.AUTO.value and message.block is not None:
            self.block_set.add(message.group)


state = SDKRequestMessageState()
_state_lock = threading.Lock()


class Handler:
    def __init__(self):
        self.logger = logging.getLogger('gomer.handler')
        self.checked = False

    def handle(self, message_queue):
        global state, _state_lock
        # live_messages = state.live_messages
        while True:
            if not message_queue.empty():
                message = json.loads(message_queue.get())
                if not self.checked:
                    if self.check_version(message):
                        continue

                message = Message.from_dict(message)
                if message.content.num in state.live_messages.keys():
                    if message.is_response():
                        if state.live_messages[message.content.num].check_response(message):
                            continue
                    elif message.is_complete():
                        if state.live_messages[message.content.num].completed:
                            continue
                        with _state_lock:
                            if state.live_messages[message.content.num].check_complete(message):
                                self.response_complete(message)
                                if state.live_messages[message.content.num].block != BlockStatus.ALL.value:
                                    state.del_item(state.live_messages[message.content.num])
                    else:
                        self.logger.info('....handler thread:do not konw the message type: ' + str(message))
            else:
                time.sleep(0.01)

    def response_complete(self, message):
        message.message_type = MessageType.RESPONSE.value
        message.code = ResultCode.SUCCESS.value
        Connection().send(str(message))

    def check_version(self, message):
        if message.get('hard') is not None:
            version = message.get('hard').get('ver')
            pattern = r'(\d+).(\d+).(\d+)'
            gomer_version = re.match(pattern, version)
            gomer_version = (
                int(gomer_version.group(1)), int(gomer_version.group(2)), int(gomer_version.group(3)))
            if gomer_version >= MINIMUM_GOMER_VERSION:
                self.checked = True
                return True
            else:
                raise GomerNeedsUpdate('Gomer version is: {}, minimun version required is: {}.{}.{}. '
                                       'You can update your gomer via Gomer Android APP.'
                                       .format(version, MINIMUM_GOMER_VERSION[0], MINIMUM_GOMER_VERSION[1],
                                               MINIMUM_GOMER_VERSION[2]))


class MessageSender:
    def __init__(self):
        self.logger = logging.getLogger('gomer.message_sender')
        global state, _state_lock

    def send_original(self, message):
        Connection().send(message)

    def send(self, message):
        self.logger.info("start message: {}".format(message))
        self.wait_for_send(message)
        Connection().send(str(message))
        with _state_lock:
            state.add_item(message)
        self.wait_for_response(message)
        self.interrupt_previous_message(message)
        if message.block == BlockStatus.ALL.value:
            while not state.live_messages[message.content.num].completed:
                time.sleep(0.01)
            self.logger.info("message complete")

            complete_content = state.live_messages[message.content.num].complete_message.content.to_dict()
            with _state_lock:
                state.del_item(message)
            return complete_content
        return None

    def wait_for_send(self, message):
        while message.group in state.block_set:
            time.sleep(0.01)

    def interrupt_previous_message(self, message):
        if message.content.num not in state.live_messages.keys():
            return False
        with _state_lock:
            for key in state.live_messages.keys():
                if key < message.content.num and state.live_messages[key].group == message.group:
                    break
                else:
                    key = None
            if key:
                state.live_messages.pop(key)

    def wait_for_response(self, message):
        id = message.content.num
        while id in state.live_messages.keys():
            if state.live_messages[id].responsed:
                return
            time.sleep(0.01)

    @staticmethod
    def upload(file_type, path):
        Connection().upload(file_type=file_type, path=path)

    def open_video(self):
        Connection().open_video()

    def close_video(self):
        Connection().close_video()

    def open_video_data(self):
        Connection().open_video_data()

    def close_video_data(self):
        Connection().close_video_data()
