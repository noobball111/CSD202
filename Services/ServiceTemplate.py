from typing import TYPE_CHECKING

# prevent circular import loops at runtime
if TYPE_CHECKING:
    from Services.Initializer import ServiceRegistry

from Utils import CustomInput
from Utils.Signal import Signal

from Shared.Signals import Signals

# Module = None

class Init:
    def __init__(self, CONTROLLERS):
        global Module
        self._CONTROLLERS = CONTROLLERS
        # Module = self