from .base_function import BaseFunction
from .counter import counter
import json


class Hardware(BaseFunction):
    def __init__(self):
        super().__init__()

    def check_version(self):
        num = counter.generate_sequence()
        message = dict(seq=num, msgtype=1, hard=dict(num=num, call=300))
        message = json.dumps(message)
        self.sender.send_original(message)
