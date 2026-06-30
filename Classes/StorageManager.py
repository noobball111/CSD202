import json
import os
import datetime as dt
from typing import Set
from .Product import Product, Attribute
from .Batch import Batch
from . import Batch as BatchModule


class   StorageManager:
    def __init__(self):
        self.Products = dict()
        self.BatchByID = dict()
        self.BatchQueue = []

        self.ProductAttributeNameCounts = {}
        self.ProductEnum = None

        # Keyword indexes
        self.ProductKeywordIndex = dict()    # key -> set of UPCs
        self.BatchKeywordIndex = dict()      # key -> set of BatchIDs
        self.ProductToBatchIndex = dict()    # ProductUPC -> set of BatchIDs

        # Numeric indexes for products (user‑defined numeric attributes)
        self.ProductNumericIndexes = dict()      # field -> list of (value, UPC)
        self.ProductDeltaNumericIndexes = dict() # field -> list of (value, UPC) for recent additions

        # Numeric indexes for batches
        self.BatchNumericIndexes = dict()        # field -> list of (value, batchID)
        self.BatchDeltaNumericIndexes = dict()   # field -> list of (value, batchID) for recent additions

    # ---------- Attribute name tracking ----------
    def _addProductAttributeName(self, field: str):
        field = field.lower()
        if field not in self.ProductAttributeNameCounts:
            self.ProductAttributeNameCounts[field] = 0
        self.ProductAttributeNameCounts[field] += 1

    def _removeProductAttributeName(self, field: str):
        field = field.lower()
        if field in self.ProductAttributeNameCounts:
            self.ProductAttributeNameCounts[field] -= 1
            if self.ProductAttributeNameCounts[field] <= 0:
                del self.ProductAttributeNameCounts[field]

    def GetProductAttributeNames(self) -> set:
        return set(self.ProductAttributeNameCounts.keys())

    def GetProductsByKeyword(self, keyword: str) -> Set[str]:
        keyword = keyword.lower()
        return self.ProductKeywordIndex.get(keyword, set())

    def GetBatchIDsByNumericComparison(self, field: str, operator: str, value: float) -> Set[int]:
        field = field.lower()
        BatchIds = set()

        def matches(v: float) -> bool:
            if operator == ">":
                return v > value
            if operator == "<":
                return v < value
            if operator == ">=":
                return v >= value
            if operator == "<=":
                return v <= value
            if operator in ("=", "=="):
                return v == value
            return False

        for IndexDict in (self.BatchNumericIndexes, self.BatchDeltaNumericIndexes):
            if field not in IndexDict:
                continue
            for v, BatchId in IndexDict[field]:
                if matches(v):
                    BatchIds.add(BatchId)

        return BatchIds

    # ---------- Product management ----------
    def AddProduct(self, product):
        """Add a product and index its attributes (both string and numeric)."""
        self.Products[product.UPC.Value] = product
        self._indexProduct(product)

    def RemoveProduct(self, product):
        """Remove a product and delete its entries from all indexes."""
        if product.UPC.Value in self.Products:
            del self.Products[product.UPC.Value]
        self._removeProduct(product)

    def GetProduct(self, upc):
        return self.Products.get(upc)

    # ---------- Batch management ----------
    def AddBatch(self, batch):
        if batch.BatchID in self.BatchByID:
            return

        BatchPosition = len(self.BatchQueue) + 1
        self._setBatchQueueDates(batch, BatchPosition)

        self.BatchByID[batch.BatchID] = batch
        self.BatchQueue.append(batch.BatchID)

        if batch.ProductUPC not in self.ProductToBatchIndex:
            self.ProductToBatchIndex[batch.ProductUPC] = set()
        self.ProductToBatchIndex[batch.ProductUPC].add(batch.BatchID)

        self._indexBatch(batch)

    def GetBatch(self, batchID: int):
        return self.BatchByID[batchID]

    def RemoveBatch(self, batchID: int):
        if batchID not in self.BatchByID:
            return
        batch = self.BatchByID.pop(batchID)

        if batchID in self.BatchQueue:
            self.BatchQueue.remove(batchID)

        self.ProductToBatchIndex[batch.ProductUPC].remove(batchID)
        if not self.ProductToBatchIndex[batch.ProductUPC]:
            del self.ProductToBatchIndex[batch.ProductUPC]

        self._removeBatch(batch)
        self._rebuildBatchQueue()

    def BulkAddBatches(self, batches):
        for batch in batches:
            if self.DoesBatchIDExist(batch):
                continue
            self.AddBatch(batch)

    def ProcessBatch(self, batchID: int, FilePath: str = "data.txt"):
        """Process (deliver) a batch by removing it from storage and saving the database."""
        if batchID not in self.BatchByID:
            return False
        self.RemoveBatch(batchID)
        return self.SaveDatabase(FilePath)

    def _setBatchQueueDates(self, batch, position: int):
        batch.QueuePosition = position
        QueueDate = batch.ImportedDate + dt.timedelta(days=position)
        batch.ExpirationDate = QueueDate
        batch.DeliveryDate = QueueDate

    def _rebuildBatchQueue(self):
        if not self.BatchQueue:
            return

        SortedQueue = sorted(
            self.BatchQueue,
            key=lambda bid: self.BatchByID[bid].QueuePosition if self.BatchByID[bid].QueuePosition is not None else self._dateToNumeric(self.BatchByID[bid].ImportedDate)
        )

        self.BatchQueue = []
        for position, batchID in enumerate(SortedQueue, start=1):
            batch = self.BatchByID[batchID]
            self._removeBatch(batch)
            self._setBatchQueueDates(batch, position)
            self._indexBatch(batch)
            self.BatchQueue.append(batchID)

    def RemoveBulkBatches(self, batchIDs):
        for batchID in batchIDs:
            self.RemoveBatch(batchID)

    def DoesBatchIDExist(self, batch):
        return batch.BatchID in self.BatchByID

    # ---------- Rebuilding indexes ----------
    def RebuildProductIndex(self):
        self.ProductKeywordIndex.clear()
        self.ProductNumericIndexes.clear()
        self.ProductDeltaNumericIndexes.clear()
        self.ProductAttributeNameCounts.clear()
        for prod in self.Products.values():
            self._indexProduct(prod)
        # Sort numeric indexes
        for index in self.ProductNumericIndexes.values():
            index.sort(key=lambda x: x[0])

    def RebuildBatchIndex(self):
        self.BatchKeywordIndex.clear()
        self.BatchNumericIndexes.clear()
        self.BatchDeltaNumericIndexes.clear()

    def SetProductEnum(self, productEnum):
        self.ProductEnum = productEnum

    def SaveDatabase(self, FilePath: str):
        payload = {
            "products": [],
            "batches": [],
            "enums": {},
            "indexes": {
                "product_keywords": {k: list(v) for k, v in self.ProductKeywordIndex.items()},
                "batch_keywords": {k: list(v) for k, v in self.BatchKeywordIndex.items()},
                "product_to_batch": {k: list(v) for k, v in self.ProductToBatchIndex.items()},
                "product_numeric": {k: v for k, v in self.ProductNumericIndexes.items()},
                "product_delta_numeric": {k: v for k, v in self.ProductDeltaNumericIndexes.items()},
                "batch_numeric": {k: v for k, v in self.BatchNumericIndexes.items()},
                "batch_delta_numeric": {k: v for k, v in self.BatchDeltaNumericIndexes.items()},
            },
        }

        if self.ProductEnum is not None:
            payload["enums"] = {
                EnumName: {
                    "type": self.ProductEnum.GetType(EnumName),
                    "values": self.ProductEnum.GetValues(EnumName),
                }
                for EnumName in self.ProductEnum.EnumNames()
            }

        for product in self.Products.values():
            ProductData = {
                "UPC": product.UPC.Value,
                "Name": product.Name.Value,
                "attributes": [
                    {
                        "name": AttrName,
                        "value": attr.Value,
                        "type": attr.Type,
                        "is_enum": attr.IsEnum,
                        "EnumName": attr.EnumName,
                    }
                    for AttrName, attr in product.__dict__.items()
                    if not AttrName.startswith("_") and isinstance(attr, Attribute)
                ],
            }
            payload["products"].append(ProductData)

        for batch in self.BatchByID.values():
            payload["batches"].append({
                "BatchID": batch.BatchID,
                "ProductUPC": batch.ProductUPC,
                "Amount": batch.Amount,
                "State": batch.State,
                "ImportedDate": batch.ImportedDate.isoformat(),
                "ExpirationDate": batch.ExpirationDate.isoformat() if batch.ExpirationDate is not None else None,
                "DeliveryDate": batch.DeliveryDate.isoformat() if batch.DeliveryDate is not None else None,
                "QueuePosition": batch.QueuePosition,
            })

        os.makedirs(os.path.dirname(FilePath) or ".", exist_ok=True)
        with open(FilePath, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
        return True

    def LoadDatabase(self, FilePath: str, productEnum=None):
        if not os.path.exists(FilePath):
            return False

        try:
            with open(FilePath, "r", encoding="utf-8") as fh:
                payload = json.load(fh)
        except (json.JSONDecodeError, ValueError, OSError) as exc:
            return False

        self.Products.clear()
        self.BatchByID.clear()
        self.BatchQueue.clear()
        self.ProductKeywordIndex.clear()
        self.BatchKeywordIndex.clear()
        self.ProductToBatchIndex.clear()
        self.ProductNumericIndexes.clear()
        self.ProductDeltaNumericIndexes.clear()
        self.BatchNumericIndexes.clear()
        self.BatchDeltaNumericIndexes.clear()
        self.ProductAttributeNameCounts.clear()

        if productEnum is not None:
            self.ProductEnum = productEnum
            self.ProductEnum._enums.clear()
        elif self.ProductEnum is not None:
            self.ProductEnum._enums.clear()

        enums = payload.get("enums", {})
        for EnumName, EnumData in enums.items():
            if self.ProductEnum is not None:
                self.ProductEnum.NewEnum(EnumName, EnumData.get("type", "string"))
                for val in EnumData.get("values", []):
                    self.ProductEnum.AddToEnum(EnumName, val)

        for ProductData in payload.get("products", []):
            product = Product(ProductData["UPC"], ProductData["Name"])
            for attr in ProductData.get("attributes", []):
                if attr["name"] in ("UPC", "Name"):
                    continue
                product.AddAttribute(
                    attr["name"],
                    attr["value"],
                    attr["type"],
                    attr["is_enum"],
                    attr.get("EnumName"),
                )
            self.Products[product.UPC.Value] = product
            self._indexProduct(product)

        MaxBatchId = -1
        for BatchData in payload.get("batches", []):
            batch = Batch(BatchData["ProductUPC"], BatchData["Amount"], BatchData["State"])
            batch.BatchID = BatchData["BatchID"]
            batch.ImportedDate = dt.datetime.fromisoformat(BatchData["ImportedDate"])
            batch.ExpirationDate = dt.datetime.fromisoformat(BatchData["ExpirationDate"]) if BatchData.get("ExpirationDate") else None
            batch.DeliveryDate = dt.datetime.fromisoformat(BatchData["DeliveryDate"]) if BatchData.get("DeliveryDate") else None
            batch.QueuePosition = BatchData.get("QueuePosition")
            self.BatchByID[batch.BatchID] = batch
            if batch.ProductUPC not in self.ProductToBatchIndex:
                self.ProductToBatchIndex[batch.ProductUPC] = set()
            self.ProductToBatchIndex[batch.ProductUPC].add(batch.BatchID)
            MaxBatchId = max(MaxBatchId, batch.BatchID)

        if self.BatchByID:
            self.BatchQueue = list(self.BatchByID.keys())
            self._rebuildBatchQueue()

        if MaxBatchId >= 0:
            BatchModule.Data["BatchID"] = MaxBatchId

        self.OptimizeDatabase()
        return True

    # ---------- Internal product index helpers ----------
    def _addToProductKeyword(self, key: str, upc: str):
        key = key.lower()
        if key not in self.ProductKeywordIndex:
            self.ProductKeywordIndex[key] = set()
        self.ProductKeywordIndex[key].add(upc)

    def _removeFromProductKeyword(self, key: str, upc: str):
        key = key.lower()
        if key in self.ProductKeywordIndex:
            self.ProductKeywordIndex[key].discard(upc)
            if not self.ProductKeywordIndex[key]:
                del self.ProductKeywordIndex[key]

    def _addToProductNumeric(self, field: str, value: int | float, upc: str, delta: bool = False):
        field = field.lower()
        target = self.ProductDeltaNumericIndexes if delta else self.ProductNumericIndexes
        if field not in target:
            target[field] = []
        target[field].append((value, upc))

    def _removeFromProductNumeric(self, field: str, value: int | float, upc: str, delta: bool = False):
        field = field.lower()
        target = self.ProductDeltaNumericIndexes if delta else self.ProductNumericIndexes
        if field in target:
            target[field] = [(v, u) for v, u in target[field] if not (v == value and u == upc)]
            if not target[field]:
                del target[field]

    def _indexProduct(self, prod):
        upc = prod.UPC.Value
        for attr, data in prod.__dict__.items():
            if attr.startswith("_"):
                continue
            if not isinstance(data, Attribute):
                continue
            # Track attribute name
            self._addProductAttributeName(attr)
            # Index the attribute name itself (e.g., "size", "price")
            self._addToProductKeyword(attr.lower(), upc)

            ValueStr = str(data.Value).lower()
            self._addToProductKeyword(ValueStr, upc)
            if data.Type == "string" and isinstance(data.Value, str):
                for token in ValueStr.split():
                    self._addToProductKeyword(token, upc)
            # Field‑specific keyword for exact field search
            self._addToProductKeyword(f"{attr.lower()}:{ValueStr}", upc)

    def _removeProduct(self, prod):
        upc = prod.UPC.Value
        for attr, data in prod.__dict__.items():
            if attr.startswith("_") or not isinstance(data, Attribute):
                continue
            self._removeProductAttributeName(attr)
            self._removeFromProductKeyword(attr.lower(), upc)
            ValueStr = str(data.Value).lower()
            self._removeFromProductKeyword(ValueStr, upc)
            if data.Type == "string" and isinstance(data.Value, str):
                for token in ValueStr.split():
                    self._removeFromProductKeyword(token, upc)
            self._removeFromProductKeyword(f"{attr.lower()}:{ValueStr}", upc)

    # ---------- Internal batch index helpers ----------
    def _addToBatchKeyword(self, key: str, batchID: int):
        key = key.lower()
        if key not in self.BatchKeywordIndex:
            self.BatchKeywordIndex[key] = set()
        self.BatchKeywordIndex[key].add(batchID)

    def _removeFromBatchKeyword(self, key: str, batchID: int):
        key = key.lower()
        if key in self.BatchKeywordIndex:
            self.BatchKeywordIndex[key].discard(batchID)
            if not self.BatchKeywordIndex[key]:
                del self.BatchKeywordIndex[key]

    def _dateToNumeric(self, DateValue: dt.datetime) -> float:
        DayValue = DateValue.toordinal()
        seconds = (
            DateValue.hour * 3600
            + DateValue.minute * 60
            + DateValue.second
            + DateValue.microsecond / 1_000_000
        )
        return DayValue + seconds / 86400.0

    def _indexBatch(self, batch, useDelta=True):
        state = batch.State.lower()
        self._addToBatchKeyword(state, batch.BatchID)
        self._addToBatchKeyword(f"state:{state}", batch.BatchID)

        if batch.ExpirationDate is None:
            self._addToBatchKeyword("noexpiration", batch.BatchID)
        else:
            self._addToBatchKeyword("hasexpiration", batch.BatchID)

        addNumeric = self._addToBatchDeltaNumeric if useDelta else self._addToBatchNumeric

        addNumeric("amount", batch.Amount, batch.BatchID)
        addNumeric("importeddate", self._dateToNumeric(batch.ImportedDate), batch.BatchID)
        if batch.ExpirationDate is not None:
            addNumeric("expirationdate", self._dateToNumeric(batch.ExpirationDate), batch.BatchID)

    def _removeBatch(self, batch):
        state = batch.State.lower()
        self._removeFromBatchKeyword(state, batch.BatchID)
        self._removeFromBatchKeyword(f"state:{state}", batch.BatchID)
        if batch.ExpirationDate is None:
            self._removeFromBatchKeyword("noexpiration", batch.BatchID)
        else:
            self._removeFromBatchKeyword("hasexpiration", batch.BatchID)

        # Remove from numeric indexes (both main and delta)
        self._removeFromBatchNumeric("amount", batch.Amount, batch.BatchID, delta=True)
        self._removeFromBatchNumeric("amount", batch.Amount, batch.BatchID, delta=False)
        self._removeFromBatchNumeric("importeddate", self._dateToNumeric(batch.ImportedDate), batch.BatchID, delta=True)
        self._removeFromBatchNumeric("importeddate", self._dateToNumeric(batch.ImportedDate), batch.BatchID, delta=False)
        if batch.ExpirationDate is not None:
            self._removeFromBatchNumeric("expirationdate", self._dateToNumeric(batch.ExpirationDate), batch.BatchID, delta=True)
            self._removeFromBatchNumeric("expirationdate", self._dateToNumeric(batch.ExpirationDate), batch.BatchID, delta=False)

    def _addToBatchNumeric(self, field: str, value: int | float, batchID: int):
        field = field.lower()
        if field not in self.BatchNumericIndexes:
            self.BatchNumericIndexes[field] = []
        self.BatchNumericIndexes[field].append((value, batchID))

    def _addToBatchDeltaNumeric(self, field: str, value: int | float, batchID: int):
        field = field.lower()
        if field not in self.BatchDeltaNumericIndexes:
            self.BatchDeltaNumericIndexes[field] = []
        self.BatchDeltaNumericIndexes[field].append((value, batchID))

    def _removeFromBatchNumeric(self, field: str, value: int | float, batchID: int, delta: bool):
        field = field.lower()
        target = self.BatchDeltaNumericIndexes if delta else self.BatchNumericIndexes
        if field in target:
            target[field] = [(v, b) for v, b in target[field] if not (v == value and b == batchID)]
            if not target[field]:
                del target[field]

    def OptimizeDatabase(self):
        """Merge delta numeric indexes (both product and batch) into their main sorted indexes."""
        # Merge product delta into product main
        for field, delta in self.ProductDeltaNumericIndexes.items():
            if field not in self.ProductNumericIndexes:
                self.ProductNumericIndexes[field] = []
            self.ProductNumericIndexes[field].extend(delta)
            self.ProductNumericIndexes[field].sort(key=lambda x: x[0])
        self.ProductDeltaNumericIndexes.clear()

        # Merge batch delta into batch main
        for field, delta in self.BatchDeltaNumericIndexes.items():
            if field not in self.BatchNumericIndexes:
                self.BatchNumericIndexes[field] = []
            self.BatchNumericIndexes[field].extend(delta)
            self.BatchNumericIndexes[field].sort(key=lambda x: x[0])
        self.BatchDeltaNumericIndexes.clear()