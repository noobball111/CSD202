from Utils import CustomInput
from Utils.Signal import Signal

from Classes.Queue import Queue
from Classes.Stack import Stack
from Classes.Node import Node

from Shared.Signals import Signals

Module = None

newQueue = Queue()

class Init:
    def __init__(self, CONTROLLERS):
        global Module
        self._CONTROLLERS = CONTROLLERS
        Module = self

        self.Queue = Queue


def ItemAdded(Item):
    newQueue.enqueue(Item)

    pass

def OrderProcessed(Item):
    pass
    

Signals.ItemAdded.Connect(ItemAdded)
Signals.OrderProcessed.Connect(OrderProcessed)