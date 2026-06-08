from typing import TYPE_CHECKING

# prevent circular import loops at runtime
if TYPE_CHECKING:
    from Controller.Initializer import ServiceRegistry

from Utils import CustomInput
from Utils.Signal import Signal

Module = None

class Init:
    def __init__(self, CONTROLLERS):
        global Module
        self._CONTROLLERS = CONTROLLERS
        Module = self