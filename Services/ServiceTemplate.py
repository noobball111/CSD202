from typing import TYPE_CHECKING

# prevent circular import loops at runtime
if TYPE_CHECKING:
    from Services.Initializer import ServiceRegistry as ServicesRegistery
    from Controller.Initializer import ServiceRegistry as ControllersRegistery


from Utils import CustomInput
from Utils.Signal import Signal

from Shared.Signals import Signals

# Module = None

Controllers: ControllersRegistery
Services: ServicesRegistery

class Init:
    def __init__(self, SERVICES: ServicesRegistery, CONTROLLERS: ControllersRegistery):
        global Controllers
        global Services
        Controllers = CONTROLLERS
        Services = SERVICES

        global Module
        self._SERVICES = SERVICES
        # Module = self