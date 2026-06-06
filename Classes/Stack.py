class Stack:
    def __init__(self) -> None:
        self.arr = []
    
    # Method

    def push(self, val) -> None:
        self.arr.append(val)
    
    def pop(self):
        return self.arr.pop(-1)


    # Attribute
    def Size(self) -> int:
        return len(self.arr)
    