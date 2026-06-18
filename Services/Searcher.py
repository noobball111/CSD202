from typing import TYPE_CHECKING

from Utils import CustomInput
from Utils.Signal import Signal
from Shared.Signals import Signals

class Init:
    def __init__(self, SERVICES, CONTROLLERS):
        self.Item = {}
    
    def SearchByUPC(self, UPC: int):
        Signals.Search.ByUPC

    def SearchBySKU(self, SKU: str):
        Signals.Search.BySKU

    def SearchByProduct(self, Name: str):
        Signals.Search.ByProduct

    def SearchByCategory(self, Name: str):
        Signals.Search.ByCategory
    