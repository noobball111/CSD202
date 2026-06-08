from dataclasses import dataclass
from Utils.Signal import Signal

@dataclass
class SignalsContainer:
    ItemAdded: Signal = Signal.new()
    ItemDeleting: Signal = Signal.new()
    ItemEdited: Signal = Signal.new()
    OrderProcessed: Signal = Signal.new()
    

# Create shared instance
Signals = SignalsContainer()