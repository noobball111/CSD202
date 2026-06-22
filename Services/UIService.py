import copy

from imgui_bundle import imgui, hello_imgui, ImVec4, em_to_vec2, em_size
from typing import TYPE_CHECKING

from Utils import CustomInput
from Utils.Signal import Signal

from Classes import Product

class ProductEditor:
    def __init__(self):
        self.ToBeProducts = []

        self._productTemplate = {
            "UPC": {"Value": "", "Type": "string"}, 
            "Name": {"Value": "", "Type": "string"}, 
        }
        self._productBaseFieldName = "__field__"
        self._productBaseValue = {
            "string": "text",
            "int": 0,
            "float": 0,
            "bool": True,
        }

    def _getFieldNoCollision(self, tbProd):
        fieldName = self._productBaseFieldName
        idx = 0
        while fieldName in tbProd:
            idx += 1
            fieldName = f"{fieldName}{idx}"

        return fieldName
        

    def ShowToBeProducts(self):
        for i, tbProd in enumerate(self.ToBeProducts):
            imgui.push_id(f"ToBeProduct{i}")

            imgui.text(f"New Product {i}")

            for key, data in tbProd.items():
                # Field name input text
                imgui.push_id(f"Field{key}")

                imgui.set_next_item_width(em_size(3))
                fieldKeyChanged, fieldKey = imgui.input_text("Field name", key if not self._productBaseFieldName in key else "")
                if fieldKeyChanged and imgui.is_item_deactivated_after_edit():
                    if fieldKey in tbProd:
                        fieldKey = key
                    else:
                        tbProd[fieldKey] = data
                        del tbProd[key]

                    print(tbProd)

                # Field value input text
                imgui.same_line()
                imgui.set_next_item_width(em_size(3))
                fieldValueChanged, fieldValue = imgui.input_text("Field value", data["Value"])
                if fieldValueChanged and imgui.is_item_deactivated_after_edit():
                    tbProd[fieldKey].Value = fieldValue

                    print(tbProd)

                # Delete button
                imgui.push_style_color(0, ImVec4(1.0, 0.0, 0.0, 1.0))
                imgui.push_style_color(1, ImVec4(1.0, 0.3, 0.3, 1.0))
                imgui.push_style_color(2, ImVec4(0.6, 0.0, 0.0, 1.0))

                imgui.same_line()
                if imgui.button("X"):
                    self.ToBeProducts.remove(tbProd)

                imgui.pop_style_color(3)

                imgui.pop_id()

            # Add field button
            if imgui.button("Add Field"):
                imgui.set_next_window_pos(imgui.get_mouse_pos())
                imgui.open_popup("AddFieldPopup")

            if imgui.begin_popup("AddFieldPopup"):
                for type, defaultVal in self._productBaseValue.items():
                    if imgui.selectable(type, False)[0]:
                        tbProd[self._getFieldNoCollision(tbProd)] = {
                            "Value": defaultVal,
                            "Type": type,
                        }

            imgui.pop_id()


    def Draw(self):
        imgui.text("PRODUCTS: ")
        imgui.same_line()
        if imgui.button("+"):
            self.ToBeProducts.append(copy.deepcopy(self._productTemplate))

        imgui.separator()
        self.ShowToBeProducts()
        


class MainApp:
    def __init__(self):
        self.Filter = imgui.TextFilter()

        self.ProductEditor = ProductEditor()

    def Draw(self):
        if imgui.begin_tab_bar("MainTab"):
            opened, visible = imgui.begin_tab_item("Product Editor")
            if opened: 
                self.ProductEditor.Draw()
                imgui.text("HELLPPPPP")
            
            imgui.end_tab_item()

        imgui.end_tab_bar()
            

        # self.Filter.draw('Search ("incl,-excl") ("error")', em_size(25))

        # if imgui.button("Add Product"):
        #     self.ToBeItems.append({
        #         "Name": "",
        #         "TypeIndex": 0,
        #     })

        # for toBeItem in self.ToBeItems:
        #     imgui.push_id("Enter name")

        #     imgui.set_next_item_width(em_size(5))
        #     changed, toBeItem["Name"] = imgui.input_text("Enter name", toBeItem["Name"])

        #     imgui.same_line()
        #     _, toBeItem["TypeIndex"] = imgui.combo("Type", toBeItem["TypeIndex"], ItemTypes)
            
        #     imgui.pop_id()

        # imgui.button("Remove Product")
    
        

class Init:
    def __init__(self, storageManager, productEnum):
        self.MainApp = MainApp()
        self.StorageManager = storageManager
        self.ProductEnum = productEnum

        def gui():
            self.MainApp.Draw()

        hello_imgui.run(gui, window_title="Warehouse Management System")