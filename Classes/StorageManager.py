from .Product import Product
from .Batch import Batch

class StorageManager:
    def __init__(self):
        self.Products = dict()
        self.BatchByID = dict()

        # All are InvertedIndex to help search be faster
        self.ProductKeywordIndex = dict()
        self.BatchKeywordIndex = dict()
        self.ProductToBatchIndex = dict()

        # Each field correspond to numeric index (because we allow users to create them) (sorted)
        self.NumericIndexes = dict()
        # We store other indexes for recent additions so we dont need to resort the entire thing every time (unsorted)
        self.DeltaNumericIndexes = dict()

    def AddProduct(self, product):
        self.Products[product.UPC] = product

    def RemoveProduct(self, product):
        del self.Products[product.UPC]

    def GetProduct(self, upc):
        return self.Products.get(upc)

    def GetBatch(self, batchID: int):
        return self.BatchByID.get(batchID)

    def AddBatch(self, batch):
        if batch.BatchID in self.BatchByID:
            return

        self.BatchByID[batch.BatchID] = batch

        if batch.ProductUPC not in self.ProductToBatchIndex:
            self.ProductToBatchIndex[batch.ProductUPC] = set()

        self.ProductToBatchIndex[batch.ProductUPC].add(batch.BatchID)

        self._indexBatch(batch)

    def RemoveBatch(self, batchID: int):
        if batchID not in self.BatchByID:
            return

        batch = self.BatchByID.pop(batchID)

        self.ProductToBatchIndex[batch.ProductUPC].remove(batchID)

        if not self.ProductToBatchIndex[batch.ProductUPC]:
            del self.ProductToBatchIndex[batch.ProductUPC]

    def BulkAddBatches(self, batches):
        for batch in batches:
            if self.DoesBatchIDExist(batch):
                continue

            self.AddBatch(batch)

    def RemoveBulkBatches(self, batchIDs):
        for batchID in batchIDs:
            self.RemoveBatch(batchID)

    def DoesBatchIDExist(self, batch):
        return batch.BatchID in self.BatchByID
    
    def RebuildProductIndex(self):
        self.ProductKeywordIndex.clear()

        for prod in Product.ProductCache:
            self._indexProduct(prod)

    def _addToProductIndex(self, key: str, upc: int):
        key = key.lower()

        if key not in self.ProductKeywordIndex:
            self.ProductKeywordIndex[key] = set()

        self.ProductKeywordIndex[key].add(upc)

    def _indexProduct(self, prod):
        for attr, data in prod.__dict__.items():
            if not isinstance(data.Value, str): continue

            value = str(data.Value).lower()
            field = attr.lower()

            # General keyword
            self._addToProductIndex(value, prod.UPC.Value)
            for token in value.split():
                self._addToProductIndex(token, prod.UPC.Value)

            # Field-specific keyword
            self._addToProductIndex(f"{field}:{value}", prod.UPC.Value)

    def RebuildBatchIndex(self):
        self.BatchKeywordIndex.clear()
        self.NumericIndexes.clear()
        self.DeltaNumericIndexes.clear()

        for batch in self.BatchByID.values():
            self._indexBatch(batch, useDelta=False)

        for index in self.NumericIndexes.values():
            index.sort(key=lambda x: x[0])

    def _addToBatchIndex(self, key: str, batchID: int):
        key = key.lower()

        if key not in self.BatchKeywordIndex:
            self.BatchKeywordIndex[key] = set()

        self.BatchKeywordIndex[key].add(batchID)

    def _indexBatch(self, batch, useDelta=True):
        state = batch.State.lower()

        self._addToBatchIndex(state, batch.BatchID)
        self._addToBatchIndex(f"state:{state}", batch.BatchID)

        if batch.ExpirationDate is None:
            self._addToBatchIndex("noexpiration", batch.BatchID)
        else:
            self._addToBatchIndex("hasexpiration", batch.BatchID)

        addNumeric = (self._addToDeltaNumericIndex if useDelta else self._addToNumericIndex)

        addNumeric("amount", batch.Amount, batch.BatchID)
        addNumeric("importeddate", batch.ImportedDate.timestamp(), batch.BatchID)

        if batch.ExpirationDate is not None:
            addNumeric("expirationdate", batch.ExpirationDate.timestamp(), batch.BatchID)

    def _addToNumericIndex(self, field: str, value: int | float, batchID: int):
        field = field.lower()

        if field not in self.NumericIndexes:
            self.NumericIndexes[field] = []

        self.NumericIndexes[field].append((value, batchID))

    def _addToDeltaNumericIndex(self, field: str, value: int | float, batchID: int):
        field = field.lower()

        if field not in self.DeltaNumericIndexes:
            self.DeltaNumericIndexes[field] = []

        self.DeltaNumericIndexes[field].append((value, batchID))

    def OptimizeDatabase(self):
        for field, delta in self.DeltaNumericIndexes.items():
            if field not in self.NumericIndexes:
                self.NumericIndexes[field] = []

            self.NumericIndexes[field].extend(delta)
            self.NumericIndexes[field].sort(key=lambda x: x[0])

        self.DeltaNumericIndexes.clear()
        
    