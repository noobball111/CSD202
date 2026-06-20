class ProductEnum:
    def __init__(self):
        self._lists = {}
        self._sets = {}

    def newEnum(self, enumName: str):
        if not self._enumExist(enumName): return
        
        self._lists[enumName] = list()
        self._sets[enumName] = set()

    def AddToEnum(self, enumName: str, value: str):
        if not self._enumExist(enumName): return
        
        self._lists[enumName].append(value)
        self._sets[enumName].add(value)

    def RemoveFromEnum(self, enumName: str, value: str):
        if not self._enumExist(enumName): return

        self._lists[enumName].remove(value)
        self._sets[enumName].remove(value)

    def iter(self, enumName: str):
        if not self._enumExist(enumName): return
        
        return iter(self._lists[enumName])
    
    def _enumExist(self, enumName: str):
        return enumName in self._sets
    

