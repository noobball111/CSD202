from Services.Initializer import Init as ServiceLoader
from Controller.Initializer import Init as ControllerLoader

# The very first time you run this, it creates "Initializer.pyi"
# Your IDE reads that hidden file and unlocks full autocomplete instantly
Services = ServiceLoader.load()
Controller = ControllerLoader.load()

# Controller.OrderManager