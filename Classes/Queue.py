from .Node import Node

class Queue:
    def __init__(self) -> None:
        self.Head: Node|None = None
        self.Tail: Node|None = None
        self.size = 0

    def enqueue(self, val):
        newNode = Node(val)

        if self.size == 0:
            self.Head = newNode
            self.Tail = newNode
        else:
            self.Tail.Next = newNode
            newNode.Prev = self.Tail
            self.Tail = newNode

        self.size += 1
    
    def dequeue(self):
        self.Tail = self.Tail.Prev

    
    def Size(self, val):
        return self.size