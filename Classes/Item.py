def GenerateSKU(ItemClass) -> str | None:
    if isinstance(ItemClass, Clothes):
        return f"{ItemClass.Category}-{ItemClass.Name}-{ItemClass.Size}-{ItemClass.Size}-{ItemClass.Color}"
    elif isinstance(ItemClass, Item):
        return f"{ItemClass.Category}-{ItemClass.Name}"
    
    return None

class Item:
    def __init__(self, Name, Category, Exp, Amount, UPC: int|None = None) -> None:
        self.Name = Name
        self.Category = Category
        self.Expiration = Exp
        self.Stock = Amount
        self.UPC = UPC
        self.SKU = None
        self.Type = "Item"

    def GenerateSKU(self) -> str | None:
        self.SKU = GenerateSKU(self)
        return self.SKU

class Clothes(Item):
    def __init__(self, Name, Category, Exp, Amount, UPC: int, Size, Color):
        super().__init__(Name, Category, Exp, Amount, UPC)

        self.Size = Size
        self.Color = Color
        self.Type = "Clothes"