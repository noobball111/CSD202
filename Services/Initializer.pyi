import Services.Modules.StorageManager as StorageManager
import Services.Modules.Searcher as Searcher
import Services.Modules.OrderManager as OrderManager
import Services.Modules as ModulesPackage

class ServiceRegistry:
    @property
    def OrderManager(self) -> OrderManager: ...
    @property
    def Searcher(self) -> Searcher: ...
    @property
    def StorageManager(self) -> StorageManager: ...

class Init:
    @classmethod
    def load(cls) -> ServiceRegistry: ...