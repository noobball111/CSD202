from Utils import CustomInput
from Utils.Signal import Signal

OrderController = None

class Init:
    def __init__(self, CONTROLLERS):
        global OrderController
        self._CONTROLLERS = CONTROLLERS
        OrderController = self

    def test(self, arg):
        print(arg)