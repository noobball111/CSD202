from typing import TYPE_CHECKING

# prevent circular import loops at runtime
if TYPE_CHECKING:
    from Services.Initializer import ServiceRegistry

from Utils import CustomInput
from Utils.Signal import Signal

Module = None

class Init:
    def __init__(self, CONTROLLERS: ServiceRegistry):
        global Module
        self._CONTROLLERS = CONTROLLERS
        Module = self

        self.Item = {}
    
    def SearchByUPC(self, UPC: int):
        return self._CONTROLLERS.StorageManager.LookUpbyUPC[UPC]

    def SearchBySKU(self, SKU: str):
        return self._CONTROLLERS.StorageManager.LookUpbySKU[SKU]

    def SearchByProduct(self, Name: str):
        return self._CONTROLLERS.StorageManager.LookUpByName[Name]

    def SearchByCategory(self, Name: str):
        return self._CONTROLLERS.StorageManager.CategoryOrder[Name]