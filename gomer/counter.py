import threading


class Counter(object):
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Counter, '_instance'):
            with Counter._instance_lock:
                if not hasattr(Counter, '_instance'):
                    Counter._instance = object.__new__(cls)
        return Counter._instance

    def __init__(self):
        self.__sequence = 1000

    def generate_sequence(self):
        self.__sequence += 1
        return self.__sequence

    def get_sequence(self):
        return self.__sequence


counter = Counter()
