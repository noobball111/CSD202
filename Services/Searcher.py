from typing import TYPE_CHECKING

# prevent circular import loops at runtime
if TYPE_CHECKING:
    from Services.Initializer import ServiceRegistry as ServicesRegistery
    from Controller.Initializer import ServiceRegistry as ControllersRegistery

from Utils import CustomInput
from Utils.Signal import Signal

Module = None

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