from typing import TYPE_CHECKING

# prevent circular import loops at runtime
if TYPE_CHECKING:
    from Services.Initializer import ServiceRegistry

from Utils import CustomInput
from Utils.Signal import Signal

from Classes.Queue import Queue
from Classes.Stack import Stack
from Classes.Node import Node
from Classes.Order import Order as OrderClass

from Shared.Signals import Signals

# Module = None
CONTROLLERS: ServiceRegistry = None

newQueue = Queue()
OrderLookUp = {}
ItemLookUp = {}

class Init:
    def __init__(self, Controllers: ServiceRegistry):
        global Module
        global CONTROLLERS
        self.CONTROLLERS = Controllers
        CONTROLLERS = Controllers
        # Module = self

        self.Queue = Queue


def CreateOrder(Item, Amount):
    return OrderClass(Item, Amount)

def ProcessOrder(Order: OrderClass):
    # Once an order is processed, remove them from order and storage
    Item = ItemLookUp[Order.ID]
    
    CONTROLLERS.StorageManager.AddStock(Item, Order.Amount*-1)
    newQueue.dequeue()

def ItemAdded(Item, Amount):
    newOrder = CreateOrder(Item, Amount)
    newQueue.enqueue(newOrder)

    ItemLookUp[newOrder.ID] = Item

    try:
        OrderLookUp[Item.SKU].append(newOrder)
    except:
        OrderLookUp[Item.SKU] = [newOrder]


def ItemRemoving(Item):
    # This is only for removing without processing through order (force-removing)
    # ensure to remove from: Order, Storage
    Orders = OrderLookUp[Item.SKU]

    for order in Orders:
        Queue.Remove(order)

# should never run
def ItemRemoved(Item):
    pass
    
def OrderProcessed(Item):
    # This should always match with the latest order

    pass
    

Signals.ItemAdded.Connect(ItemAdded)
Signals.ItemRemoving.Connect(ItemRemoving)
# Signals.OrderProcessed.Connect(OrderProcessed)