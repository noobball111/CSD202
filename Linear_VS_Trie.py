import time
from Classes.StorageManager import StorageManager
from Classes.Product import Attribute
from Classes.ProductEnum import ProductEnum


def build_product_keyword_sets(products):
    keyword_sets = []
    for product in products:
        keywords = set()
        for attr_name, data in product.__dict__.items():
            if attr_name.startswith("_") or not isinstance(data, Attribute):
                continue

            keywords.add(attr_name.lower())
            value_str = str(data.Value).lower()
            keywords.add(value_str)
            if data.Type == "string" and isinstance(data.Value, str):
                keywords.update(value_str.split())
            keywords.add(f"{attr_name.lower()}:{value_str}")
        keyword_sets.append(keywords)
    return keyword_sets


def build_batch_keyword_sets(batches):
    keyword_sets = []
    for batch in batches:
        keywords = {
            str(batch.BatchID).lower(),
            str(batch.Amount).lower(),
            batch.State.lower(),
            f"state:{batch.State.lower()}",
            f"amount:{batch.Amount}",
            "noexpiration" if batch.ExpirationDate is None else "hasexpiration",
        }
        keyword_sets.append(keywords)
    return keyword_sets


def benchmark_linear_products(product_keyword_sets, queries):
    start = time.perf_counter()
    for query in queries:
        matches = [keywords for keywords in product_keyword_sets if query.lower() in keywords]
        _ = len(matches)
    elapsed = time.perf_counter() - start
    return elapsed


def benchmark_linear_batches(batch_keyword_sets, queries):
    start = time.perf_counter()
    for query in queries:
        matches = [keywords for keywords in batch_keyword_sets if query.lower() in keywords]
        _ = len(matches)
    elapsed = time.perf_counter() - start
    return elapsed


def benchmark_inverted_products(storage_manager, queries):
    start = time.perf_counter()
    for query in queries:
        matches = storage_manager.GetProductsByKeyword(query)
        _ = len(matches)
    elapsed = time.perf_counter() - start
    return elapsed


def benchmark_inverted_batches(storage_manager, queries):
    start = time.perf_counter()
    for query in queries:
        matches = storage_manager.BatchKeywordIndex.get(query.lower(), set())
        _ = len(matches)
    elapsed = time.perf_counter() - start
    return elapsed


def main():
    product_enum = ProductEnum()
    storage_manager = StorageManager()
    storage_manager.SetProductEnum(product_enum)

    loaded = storage_manager.LoadDatabase("data.txt", product_enum)
    if not loaded:
        raise RuntimeError("Failed to load data.txt")

    products = list(storage_manager.Products.values())
    batches = list(storage_manager.BatchByID.values())
    product_queries = list(storage_manager.ProductKeywordIndex.keys())
    batch_queries = list(storage_manager.BatchKeywordIndex.keys())
    if len(product_queries) > 10000:
        product_queries = product_queries[:10000]
    if len(batch_queries) > 10000:
        batch_queries = batch_queries[:10000]

    product_keyword_sets = build_product_keyword_sets(products)
    batch_keyword_sets = build_batch_keyword_sets(batches)

    linear_products = benchmark_linear_products(product_keyword_sets, product_queries)
    inverted_products = benchmark_inverted_products(storage_manager, product_queries)
    linear_batches = benchmark_linear_batches(batch_keyword_sets, batch_queries)
    inverted_batches = benchmark_inverted_batches(storage_manager, batch_queries)

    print(f"Loaded products: {len(products)}")
    print(f"Loaded batches: {len(batches)}")
    print(f"Product queries tested: {len(product_queries)}")
    print(f"Batch queries tested: {len(batch_queries)}")
    print(f"Product linear scan total: {linear_products:.6f}s")
    print(f"Product inverted index total: {inverted_products:.6f}s")
    print(f"Batch linear scan total: {linear_batches:.6f}s")
    print(f"Batch inverted index total: {inverted_batches:.6f}s")
    if inverted_products > 0:
        print(f"Product speedup: {linear_products / inverted_products:.2f}x")
    if inverted_batches > 0:
        print(f"Batch speedup: {linear_batches / inverted_batches:.2f}x")


if __name__ == "__main__":
    main()
