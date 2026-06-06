from .Node import Node

class Queue:
    def __init__(self) -> None:
        self.Head: Node = None
        self.Tail: Node = None
        self.Size = 0

    def enqueue(self, val):
        if self.Size == 0:
            self.Head = val
            self.Tail = val
        else:
            self.Tail.Next = val
            self.Tail = val
    
    def dequeue(self):
        self.Tail = self.Tail.Prev

    
    def Size(self, val):
        return self.Size