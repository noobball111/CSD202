from dataclasses import dataclass, field
from Utils.Signal import Signal

@dataclass
class SearchSignal:
    BySKU: Signal = Signal.new() 
    ByUPC: Signal = Signal.new()
    ByProduct: Signal = Signal.new()
    ByCategory: Signal = Signal.new()
    

@dataclass
class SignalsContainer:

    # Item events
    ItemAdded: Signal = Signal.new()
    ItemRemoving: Signal = Signal.new()
    ItemEdited: Signal = Signal.new()
    OrderProcessed: Signal = Signal.new()

    # Search
    Search: SearchSignal = field(default_factory=SearchSignal)

# Create shared instance
Signals = SignalsContainer()