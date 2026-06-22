from dataclasses import dataclass
from typing import Literal
from Shared.Signals import Signals

Keywords = {"UPC", "SKU", "Name"}
# ProductCache = list()

# def AttributeStillExist(name: str):
#     for product in ProductCache:
#         for attr in product.__dict__.keys():
#             if attr == name: return True

#     return False

@dataclass
class Attribute:
    Value: object
    Type: Literal["string", "int", "float", "bool"]
    IsEnum: bool

class Product:
    def __init__(self, UPC: str, name: str) -> None:
        self.UPC = Attribute(UPC, "string", False)
        self.Name = Attribute(name, "string", False)
        self.GenerateSKU()

        # ProductCache.append(self)

    def AddAttribute(self, name: str, value: object, type: Literal["string", "int", "float", "bool"], isEnum: bool):
        if hasattr(self, name):
            return

        if not name in Keywords:
            Keywords.add(name)
            Signals.OnKeywordAdded.Fire(name)

        setattr(self, name, Attribute(value, type, isEnum))
        self.GenerateSKU()

    def EditAttribute(self, name: str, value: object, type: Literal["string", "int", "float", "bool"] = None, isEnum: bool = None):
        if not hasattr(self, name):
            return

        setattr(self, name, Attribute(value, type or self[name].Type, isEnum or self[name].IsEnum))
        self.GenerateSKU()

    def RemoveAttribute(self, name: str):
        if not hasattr(self, name):
            return
        
        if name in Keywords and not AttributeStillExist(name):
            Keywords.remove(name)
            Signals.OnKeywordRemoved.Fire(name)
        
        delattr(self, name)

    def GenerateSKU(self) -> str:
        self.SKU = Attribute(f"{self.UPC.Value}-{self.Name.Value}", "string", False)

    def Display(self):
        for attr, value in self.__dict__.items():
            print(attr, value)

# Test
# newProduct = Product("aaaa", "bbbb")
# newProduct.AddAttribute("Size", "XL", "string", True)

# print(newProduct.Display())