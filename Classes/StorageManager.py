from Classes import Product, Batch

class StorageManager:
    def __init__(self):
        self.Batches = list()

        # All are InvertedIndex to help search be faster
        self.ProductKeywordIndex = dict()
        self.BatchKeywordIndex = dict()
        self.ProductToBatchIndex = dict()

        self.AmountIndex = list()
        self.ExpirationDateIndex = list()
        self.ImportedDateIndex = list()

        # For checking ID collisions
        self._batchIDSet = set()

    def AddBatch(self, batch):
        if self.DoesBatchIDExist(batch):
            return
        
        self.Batches.append(batch)

    def BulkAddBatches(self, batches):
        for batch in batches:
            if self.DoesBatchIDExist(batch):
                continue

            self.AddBatch(batch)

    def DoesBatchIDExist(self, batch):
        return batch.ID in self._batchIDSet
    
    def BuildProductIndex(self):
        for keyword in Product.Keywords:
            self.AddNewProductKeyword(keyword)
            
    def AddNewProductKeyword(self, keyword: str):
        newList = list()

        for prod in Product.ProductCache:
            for attr, value in prod.__dict__.items():
                # Check attribute name for keyword
                if keyword == attr.lower():
                    newList.append(prod.UPC.Value)
                    break

                # Check value for keyword only if it's an EnumList
                if value.IsEnum and keyword == f"{value}".lower():
                    newList.append(prod.UPC.Value)
                    break

        self.ProductKeywordIndex[keyword] = newList

    