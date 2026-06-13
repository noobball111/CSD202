from Services.Initializer import Init as ServiceLoader
from Controller.Initializer import Init as ControllerLoader

# The very first time you run this, it creates "Initializer.pyi"
# Your IDE reads that and should enable numtype
Services = ServiceLoader.load()
Controller = ControllerLoader.load()

# Originally, it was OrderController.Module if you follow the template, so it could be anything
# That is why you should assign a ref
OrderController = Controller.OrderController.OrderController
UIController = Controller.UIController.Module

# DO NOT CALL Init() Controller.<Module>.Init()

OrderController.test("abc")
UIController.start()