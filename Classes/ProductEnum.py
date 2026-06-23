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
        self._enums = {}  # {enum_name: {"type": str, "values": {value: None}}}

    def NewEnum(self, enumName: str, enum_type: str = "string"):
        if enumName in self._enums:
            return
        if enum_type not in ("string", "int", "float", "bool"):
            raise ValueError("enum_type must be one of: string, int, float, bool")
        self._enums[enumName] = {"type": enum_type, "values": {}}

    def GetType(self, enumName: str) -> str:
        return self._enums.get(enumName, {}).get("type", "string")

    def _ConvertValue(self, enumName: str, value):
        enum_type = self.GetType(enumName)
        if enum_type == "string":
            return str(value)
        elif enum_type == "int":
            try:
                return int(value)
            except (ValueError, TypeError):
                return value
        elif enum_type == "float":
            try:
                return float(value)
            except (ValueError, TypeError):
                return value
        elif enum_type == "bool":
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                if value.lower() in ("true", "1", "yes", "on"):
                    return True
                if value.lower() in ("false", "0", "no", "off"):
                    return False
            return bool(value)
        return value

    def AddToEnum(self, enumName: str, value):
        if enumName not in self._enums:
            return
        converted = self._ConvertValue(enumName, value)
        self._enums[enumName]["values"][converted] = None

    def RemoveFromEnum(self, enumName: str, value):
        if enumName not in self._enums:
            return
        converted = self._ConvertValue(enumName, value)
        self._enums[enumName]["values"].pop(converted, None)

    def Exists(self, enumName: str, value) -> bool:
        if enumName not in self._enums:
            return False
        converted = self._ConvertValue(enumName, value)
        return converted in self._enums[enumName]["values"]

    def Iter(self, enumName: str):
        return iter(self._enums.get(enumName, {}).get("values", {}))

    def GetValues(self, enumName: str):
        if enumName not in self._enums:
            return []
        return list(self._enums[enumName]["values"].keys())

    def EnumExists(self, enumName: str) -> bool:
        return enumName in self._enums

    def EnumNames(self):
        return self._enums.keys()