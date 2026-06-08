from Classes import Item

def GenerateSKU(ItemClass):
    if isinstance(ItemClass, Item.Clothes):
        return f"{ItemClass.Category}-{ItemClass.Name}-{ItemClass.Size}-{ItemClass.Size}-{ItemClass.Color}"
    elif isinstance(ItemClass, Item.Item):
        return f"{ItemClass.Category}-{ItemClass.Name}"