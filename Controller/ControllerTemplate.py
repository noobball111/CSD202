from typing import TYPE_CHECKING

# prevent circular import loops at runtime
if TYPE_CHECKING:
    from Services.Initializer import ServiceRegistry as ServicesRegistery
    from Controller.Initializer import ServiceRegistry as ControllersRegistery

from Utils import CustomInput
from Utils.Signal import Signal

Module = None

class Init:
    def __init__(self, CONTROLLERS: ControllersRegistery, SERVICES: ServicesRegistery):
        global Module
        self._CONTROLLERS = CONTROLLERS
        Module = self