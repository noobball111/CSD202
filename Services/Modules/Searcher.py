from Utils import CustomInput
from Utils.Signal import Signal

Module = None

class Init:
    def __init__(self, CONTROLLERS):
        global Module
        self._CONTROLLERS = CONTROLLERS
        Module = self

        self.Item = {}
    
    def SearchByUPC(self, UPC: int):
        pass

    def SearchBySKU(self, SKU: str):
        pass

    def SearchByProduct(self, Name: str):
        pass

    def SearchByCategory(self, Name: str):
        pass