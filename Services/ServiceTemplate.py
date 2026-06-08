from Utils import CustomInput
from Utils.Signal import Signal

Module = None

class Init:
    def __init__(self, CONTROLLERS):
        global Module
        self._CONTROLLERS = CONTROLLERS
        Module = self