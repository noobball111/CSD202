##### Modules #####
from pathlib import Path
import sys


##### VARIABLES & CONSTANTS #####
Services = Path(__file__).parent.resolve() / "Modules"

SERVICES = {}

##### MAIN #####

class Initialier:
    def __init__(self):

        sys.path.append(str(Services))

        for child in Services.iterdir():
            if not child.is_file(): continue

            SERVICES[child.stem] = __import__(child.stem) #.stem to get file name without extension

        return SERVICES