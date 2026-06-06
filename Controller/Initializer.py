##### Modules #####
from pathlib import Path
import sys


##### VARIABLES & CONSTANTS #####
Controllers = Path(__file__).parent.resolve() / "Modules"

CONTROLLERS = {}

##### MAIN #####

class Initialier:
    def __init__(self):

        sys.path.append(str(Controllers))

        for child in Controllers.iterdir():
            if not child.is_file(): continue

            CONTROLLERS[child.stem] = __import__(child.stem) #.stem to get file name without extension

        return CONTROLLERS