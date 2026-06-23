from .Trie import Trie
from typing import List, Set

def debug_print(*args, **kwargs):
    print("[DEBUG SEARCH]", *args, **kwargs)

class SearchEngine:
    def __init__(self, storageManager):
        self.storageManager = storageManager
        self._mainTrie = Trie()
        self._fieldTries = {}
        self.Rebuild()

    def Rebuild(self):
        debug_print("Rebuild() started")
        self._mainTrie = Trie()
        self._fieldTries = {}

        keys = list(self.storageManager.ProductKeywordIndex.keys())
        debug_print(f"Keys from ProductKeywordIndex: {keys}")
        for key in keys:
            self._mainTrie.Add(key)

        attr_names = self.storageManager.GetProductAttributeNames()
        debug_print(f"Attribute names: {attr_names}")
        for field in attr_names:
            field = field.lower()
            field_prefix = f"{field}:"
            field_trie = Trie()
            for key in keys:
                if key.startswith(field_prefix):
                    value_part = key[len(field_prefix):]
                    field_trie.Add(value_part)
            self._fieldTries[field] = field_trie

        # Add field prefixes for autocompletion
        for field in attr_names:
            self._mainTrie.Add(f"{field.lower()}:")
        debug_print("Rebuild() finished")

    def Autocomplete(self, query: str) -> List[str]:
        query = query.strip().lower()
        if not query:
            return []

        if ":" in query:
            field, sub = query.split(":", 1)
            field = field.strip()
            sub = sub.lstrip()
            if field in self._fieldTries:
                results = self._fieldTries[field].Find(sub)
                return [f"{field}:{r}" for r in results]
            return []
        return self._mainTrie.Find(query)

    def GetSuggestions(self, query: str, limit: int = 10) -> List[str]:
        suggestions = self.Autocomplete(query)
        debug_print(f"GetSuggestions('{query}') -> {suggestions[:limit]}")
        return suggestions[:limit]