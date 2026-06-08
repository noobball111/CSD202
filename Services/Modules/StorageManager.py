from Utils import CustomInput
from Utils.Signal import Signal

from Shared.Signals import Signals

from Classes import Item

Module = None
Items = {}

class Init:
    def __init__(self, CONTROLLERS):
        global Module
        self._CONTROLLERS = CONTROLLERS
        Module = self

        self.Items = Items
    
    def Add(self, Type: str, Name: str, Category: str, Exp: int, Amount: int, UPC: int|None = None, *args):
        TargetClass = getattr(Item, Type)
        newItem: Item.Item = TargetClass(Name, Category, Exp, Amount, UPC, args)
        newSKU = newItem.GenerateSKU()
        
        if self.Existed(newSKU):
            Item = self.Existed(newSKU)

            self.AddStock(Item, Amount)
        else:
            Signals.ItemAdded.Fire(newItem)

    def Existed(self, SKU: str | None):
        return self.Items.get(SKU)

    def Remove(self, Item):
        Signals.ItemDeleting.Fire(Item)

        pass

    def Edit(self, Item, attr):
        
        Signals.ItemEdited.Fire(Item)
        pass

    def AddStock(self, Item: Item.Item, Amount):
        Item.Stock += Amount

        if Item.Stock == 0:
            Warning(f'{Item.Name} is out of stock! | {Item.SKU}')

        elif Item.Stock < 0:
            Warning(f'{Item.Name} stock is not enough | Required {Amount}, Missing {Amount - Item.Stock} | {Item.SKU}')