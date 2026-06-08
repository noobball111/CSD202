import Controller.Modules.UIController as UIController
import Controller.Modules.StorageController as StorageController
import Controller.Modules.OrderController as OrderController
import Controller.Modules as ModulesPackage

class ServiceRegistry:
    @property
    def OrderController(self) -> OrderController: ...
    @property
    def StorageController(self) -> StorageController: ...
    @property
    def UIController(self) -> UIController: ...

class Init:
    @classmethod
    def load(cls) -> ServiceRegistry: ...