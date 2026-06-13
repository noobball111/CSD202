from Services.Initializer import Init as ServiceLoader
from Controller.Initializer import Init as ControllerLoader

# The very first time you run this, it creates "Initializer.pyi"
# Your IDE reads that and should enable numtype

# Originally, it was OrderController.Module if you follow the template, so it could be anything
# That is why you should assign a ref


from Controller.Initializer import Init as ControllerLoader
from Services.Initializer import Init as ServiceLoader

Services = ServiceLoader.load()
Controller = ControllerLoader.load()

Services.Controllers = Controller
Controller.Services = Services

Services = Services.Modules
Controller = Controller.Modules

# DO NOT CALL Init() Controller.<Module>.Init()
# OrderController = Controller.OrderController.OrderController

# OrderController.test("abc")
Services.StorageManager.Module.test()