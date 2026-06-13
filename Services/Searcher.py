from typing import TYPE_CHECKING

from Utils import CustomInput
from Utils.Signal import Signal

class Init:
    def __init__(self, SERVICES, CONTROLLERS):
        global Module
        self._SERVICES = SERVICES
        Module = self

        self.Item = {}
    
    def SearchByUPC(self, UPC: int):
        return self._SERVICES.StorageManager.LookUpbyUPC[UPC]

    def SearchBySKU(self, SKU: str):
        return self._SERVICES.StorageManager.LookUpbySKU[SKU]

    def SearchByProduct(self, Name: str):
        return self._SERVICES.StorageManager.LookUpByName[Name]

    def SearchByCategory(self, Name: str):
        return self._SERVICES.StorageManager.CategoryOrder[Name]