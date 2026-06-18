from imgui_bundle import imgui, hello_imgui, em_to_vec2, em_size
from typing import TYPE_CHECKING

from Utils import CustomInput
from Utils.Signal import Signal

from Classes import Item

ItemTypes = ["Item", "Clothes"]

class MainApp:
    def __init__(self):
        self.Filter = imgui.TextFilter()
        self.ToBeItems = []

    def Draw(self):
        self.Filter.draw('Search ("incl,-excl") ("error")', em_size(25))

        if imgui.button("Add Product"):
            self.ToBeItems.append({
                "Name": "",
                "TypeIndex": 0,
            })

        for toBeItem in self.ToBeItems:
            imgui.push_id("Enter name")

            imgui.set_next_item_width(em_size(5))
            changed, toBeItem["Name"] = imgui.input_text("Enter name", toBeItem["Name"])

            imgui.same_line()
            _, toBeItem["TypeIndex"] = imgui.combo("Type", toBeItem["TypeIndex"], ItemTypes)
            
            imgui.pop_id()

        imgui.button("Remove Product")
    
        

class Init:
    def __init__(self):
        self.MainApp = MainApp()

        def gui():
            self.MainApp.Draw()

        hello_imgui.run(gui, window_title="Warehouse Management System")