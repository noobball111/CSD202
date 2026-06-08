import Controller.Modules.StorageController as StorageController
import Controller.Modules.OrderController as OrderController
import Controller.Modules as ModulesPackage

class ServiceRegistry:
    @property
    def OrderController(self) -> OrderController: ...
    @property
    def StorageController(self) -> StorageController: ...

class Init:
    @classmethod
    def load(cls) -> ServiceRegistry: ...