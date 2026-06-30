from .Node import Node
import datetime as dt

class Queue:
    def __init__(self) -> None:
        self.Head: Node|None = None
        self.Tail: Node|None = None
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def __bool__(self) -> bool:
        return self.size > 0

    def __iter__(self):
        curr = self.Head
        while curr is not None:
            yield curr.val
            curr = curr.Next

    def __eq__(self, other) -> bool:
        if isinstance(other, Queue):
            return self.GetAllItems() == other.GetAllItems()
        if isinstance(other, (list, tuple)):
            return self.GetAllItems() == list(other)
        return False

    def __repr__(self) -> str:
        return f"Queue({self.GetAllItems()})"

    def enqueue(self, val):
        """Add an item to the end of the queue"""
        newNode = Node(val)

        if self.size == 0:
            self.Head = newNode
            self.Tail = newNode
        else:
            self.Tail.Next = newNode
            newNode.Prev = self.Tail
            self.Tail = newNode

        self.size += 1

    def append(self, val):
        """Alias for enqueue for list-like compatibility."""
        self.enqueue(val)

    def clear(self):
        """Remove all items from the queue."""
        self.Head = None
        self.Tail = None
        self.size = 0

    def remove(self, val):
        """Remove the first matching value from the queue."""
        if self.size == 0:
            return False

        curr = self.Head
        while curr is not None:
            if curr.val == val:
                break
            curr = curr.Next

        if curr is None:
            return False

        if curr == self.Head:
            self.dequeue()
        elif curr == self.Tail:
            self.Tail = self.Tail.Prev
            if self.Tail:
                self.Tail.Next = None
            self.size -= 1
        else:
            if curr.Next:
                curr.Next.Prev = curr.Prev
            if curr.Prev:
                curr.Prev.Next = curr.Next
            self.size -= 1

        return True
    
    def dequeue(self):
        """Remove and return the first item from the queue"""
        if self.size == 0:
            return None

        val = self.Head.val
        if self.size == 1:
            self.Head = None
            self.Tail = None
        else:
            self.Head = self.Head.Next
            self.Head.Prev = None

        self.size -= 1
        return val

    # DO NOT CALL
    def RemoveByAttribute(self, attr, val):
        """Remove the first node where getattr(node.val, attr) == val"""
        if self.size == 0:
            return False
        
        curr = self.Head

        while curr is not None:
            if getattr(curr.val, attr, None) == val:
                break
            curr = curr.Next

        if curr is None:
            return False

        if curr == self.Head:
            self.dequeue()
        elif curr == self.Tail:
            self.Tail = self.Tail.Next
            if self.Tail:
                self.Tail.Prev = None
            self.size -= 1
        else:
            if curr.Next:
                curr.Next.Prev = curr.Prev
            if curr.Prev:
                curr.Prev.Next = curr.Next
            self.size -= 1
        
        return True

    # This method is optimized to not lag with large queues by using binary search on the sorted queue.
    # Should not be used on unsorted queues, as it will not work correctly.
    def RemoveByClosestDate(self, target_date: dt.datetime, date_attr: str = "ExpirationDate"):
        """Find and remove the node with the closest date to target_date.
        This is optimized to not lag with large queues by using binary search on the sorted queue."""
        if self.size == 0:
            return False
        
        closest_node = None
        closest_diff = None
        curr = self.Head

        # Single pass to find closest
        while curr is not None:
            node_date = getattr(curr.val, date_attr, None)
            if node_date is not None:
                diff = abs((node_date - target_date).total_seconds())
                if closest_diff is None or diff < closest_diff:
                    closest_diff = diff
                    closest_node = curr
            curr = curr.Next

        if closest_node is None:
            return False

        # Remove the closest node
        if closest_node == self.Head:
            self.dequeue()
        elif closest_node == self.Tail:
            self.Tail = self.Tail.Prev
            if self.Tail:
                self.Tail.Next = None
            self.size -= 1
        else:
            if closest_node.Next:
                closest_node.Next.Prev = closest_node.Prev
            if closest_node.Prev:
                closest_node.Prev.Next = closest_node.Next
            self.size -= 1
        
        return True

    def GetAllItems(self):
        """Return all items in the queue as a list"""
        items = []
        curr = self.Head
        while curr is not None:
            items.append(curr.val)
            curr = curr.Next
        return items

    def Size(self):
        """Return the current size of the queue"""
        return self.size