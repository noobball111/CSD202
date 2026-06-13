from typing import TYPE_CHECKING

from Utils import CustomInput
from Utils.Signal import Signal

from Shared.Signals import Signals

# Module = None

class Init:
    def __init__(self):
        global Controllers
        global Services

        global Module
        # Module = self