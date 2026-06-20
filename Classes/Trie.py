from Stack import Stack

class Node:
    def __init__(self, val) -> None:
        self.val = val
        self.IsWord = False
        self.Word = ""
        self.Words = {}
        
    def Add(self, val):
        self.Words[val] = Node(val)
        return self.Words[val]

class Trie:
    def __init__(self) -> None:
        self.Head = Node(None)

    def _TravereAll(self, StartNode):
        res = []
        newStack = Stack()
        newStack.push(StartNode)

        while newStack.size > 0:
            curr = newStack.pop()
            
            if curr.IsWord: 
                res.append(curr.Word)
                
            for char in curr.Words:
                newStack.push(curr.Words[char])
            
        return res

    def Find(self, string: str):
        string = string.strip().lower()
        curr = self.Head

        for char in string:
            if char not in curr.Words:
                return []
            curr = curr.Words[char]
        
        return self._TravereAll(curr)

    def Add(self, string: str = ""):
        if string == "": return
        string = string.strip().lower()
        curr = self.Head

        for char in string:
            if char not in curr.Words:
                curr = curr.Add(char)
            else:
                curr = curr.Words[char]

        curr.IsWord = True
        curr.Word = string