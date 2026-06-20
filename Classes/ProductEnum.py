# class ProductEnum:
#     def __init__(self):
#         self._lists = {}
#         self._sets = {}

#     def newEnum(self, enumName: str):
#         if not self._enumExist(enumName): return
        
#         self._lists[enumName] = list()
#         self._sets[enumName] = set()

#     def AddToEnum(self, enumName: str, value: str):
#         if not self._enumExist(enumName): return
        
#         self._lists[enumName].append(value)
#         self._sets[enumName].add(value)

#     def RemoveFromEnum(self, enumName: str, value: str):
#         if not self._enumExist(enumName): return

#         self._lists[enumName].remove(value)
#         self._sets[enumName].remove(value)

#     def iter(self, enumName: str):
#         if not self._enumExist(enumName): return
        
#         return iter(self._lists[enumName])
    
#     def _enumExist(self, enumName: str):
#         return enumName in self._sets
    

class ProductEnum:
    def __init__(self):
        self._enums = {}

    def NewEnum(self, enumName: str):
        if enumName in self._enums:
            return

        self._enums[enumName] = {}

    def AddToEnum(self, enumName: str, value: str):
        if enumName not in self._enums:
            return

        self._enums[enumName][value] = None

    def RemoveFromEnum(self, enumName: str, value: str):
        if enumName not in self._enums:
            return

        self._enums[enumName].pop(value, None)

    def Exists(self, enumName: str, value: str):
        if enumName not in self._enums:
            return False

        return value in self._enums[enumName]

    def Iter(self, enumName: str):
        if enumName not in self._enums:
            return iter(())

        return iter(self._enums[enumName])

    def GetValues(self, enumName: str):
        if enumName not in self._enums:
            return []

        return list(self._enums[enumName])

    def EnumExists(self, enumName: str):
        return enumName in self._enums