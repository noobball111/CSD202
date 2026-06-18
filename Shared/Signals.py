from dataclasses import dataclass, field
from Utils.Signal import Signal

@dataclass
class SearchSignals:
    BySKU: Signal = Signal.new() 
    ByUPC: Signal = Signal.new()
    ByProduct: Signal = Signal.new()
    ByCategory: Signal = Signal.new()

@dataclass
class ItemSignals:
    Added: Signal = Signal.new()
    Removing: Signal = Signal.new()
    Edited: Signal = Signal.new()
    Processed: Signal = Signal.new()    

@dataclass
class SignalsContainer:

    # Item events
    Item: ItemSignals = field(default_factory=ItemSignals)

    # Search
    Search: SearchSignals = field(default_factory=SearchSignals)

# Create shared instance
Signals = SignalsContainer()