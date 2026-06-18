from typing import TYPE_CHECKING

from Utils import CustomInput
from Utils.Signal import Signal

from Shared.Signals import Signals

from Classes import Item

Items = {}

CategoryOrder = {}
LookUpByName = {}
LookUpbySKU = {}
LookUpbyUPC = {}

# INVERTED INDEX 
class InvertedIndexSearch:
    def __init__(self, product_list):
        self.index = {}
        self.product_map = {}
        
        # Build initial index
        for p in product_list:
            self.add_product(p)
                
    def add_product(self, p):
        # If product already exists, remove its old token links first to prevent ghost matches
        if p["id"] in self.product_map:
            self.remove_product(p["id"])

        self.product_map[p["id"]] = p
        tokens = p["name"].lower().split()
        for token in tokens:
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(p["id"])

    def remove_product(self, product_id):
        if product_id not in self.product_map:
            return
            
        p = self.product_map.pop(product_id)
        tokens = p["name"].lower().split()
        
        # Scrub this ID out of every token set it belonged to
        for token in tokens:
            if token in self.index:
                self.index[token].discard(product_id)
                # Clean up empty token slots to save memory
                if not self.index[token]:
                    del self.index[token]

    def update_product(self, updated_p):
        # Updates a product (handles token adjustments if the name changed).
        # add_product() now checks for existing IDs, it can handle updates cleanly!
        self.add_product(updated_p)

    def search(self, query):
        query_tokens = query.lower().split()
        if not query_tokens:
            return []
            
        first_token = query_tokens[0]
        matched_ids = set()
        for key in self.index:
            if key.startswith(first_token):
                matched_ids.update(self.index[key])
                
        if not matched_ids:
            return []
            
        for token in query_tokens[1:]:
            token_ids = set()
            for key in self.index:
                if key.startswith(token):
                    token_ids.update(self.index[key])
            matched_ids.intersection_update(token_ids)
            if not matched_ids:
                break
                
        return [self.product_map[pid] for pid in matched_ids]

Products: list[dict[str, str]] = []


# search_query = "Pro Logitech Compact Wireless Mouse"
indexer = InvertedIndexSearch(Products)
# res2 = indexer.search(search_query)


class Init:
    def __init__(self):
        self.Items = Items
    
    # def Add(self, Type: str, Name: str, Category: str, Exp: int, Amount: int, UPC: int|None = None, *args):

    def Add(self, newItem: Item.Item):


        # TargetClass = getattr(Item, Type)
        # newItem: Item.Item = TargetClass(Name, Category, Exp, Amount, UPC, args)
        # newSKU = newItem.GenerateSKU()

        if self.Existed(newItem.SKU):
            oldItem: Item.Item = self.Existed(newItem.SKU)

            self.AddStock(oldItem, newItem.Amount)
            
        else:
            try:
                CategoryOrder[newItem.Category].append(newItem)
            except:
                CategoryOrder[newItem.Category] = [newItem]

            try:
                LookUpByName[newItem.Name].append(newItem)
            except:
                LookUpByName[newItem.Name] = [newItem]

            LookUpbySKU[newItem.SKU] = [newItem]
            LookUpbyUPC[newItem.SKU] = [newItem]

            indexer.add_product(newItem.Name)

            # Signals.ItemAdded.Fire(newItem, Amount)
        
        Signals.Item.Added.Fire(newItem, newItem.Amount)


    def Existed(self, SKU: str | None) -> Item.Item:
        return self.Items.get(SKU) # pyright: ignore[reportReturnType]

    def Remove(self, Item: Item.Item):
        Signals.Item.Removing.Fire(Item)

        CategoryOrder[Item.Category].remove(Item)
        LookUpByName[Item.Name].remove(Item)
        LookUpbySKU[Item.SKU] = None
        LookUpbyUPC[Item.UPC] = None
        indexer.remove_product(Item.UPC)

        Items[Item.SKU] = None

    
    def Edit(self, Item: Item.Item, attr, value):
        if not self.Existed(Item.SKU): return
        if not getattr(Item, attr): return

        setattr(Item, attr, value)

        Signals.ItemEdited.Fire(Item, attr, value)

    def AddStock(self, Item: Item.Item, Amount):
        Item.Stock += Amount

        if Item.Stock == 0:
            self.Remove(Item)
            Warning(f'{Item.Name} is out of stock! | {Item.SKU}')

        elif Item.Stock < 0:
            Warning(f'{Item.Name} stock is not enough | Required {Amount}, Missing {Amount - Item.Stock} | {Item.SKU}')
            Item.Stock += Amount*-1

def Edit(Item, attr, val):
    # if not Module: return

    # Module.Edit(Item, attr, val)

    Signals.Item.Edit.Fire(Item, attr, val)

def AddStock(Item, Amount):
    # if not Module: return

    # Module.AddStock(Item, Amount)
    Signals.Item.AddStock.Fire(Item, Amount)