import copy

from imgui_bundle import imgui, hello_imgui, ImVec4, em_to_vec2, em_size
from typing import TYPE_CHECKING

from Utils import CustomInput
from Utils.Signal import Signal

from Classes import Product

class EnumEditor:
    def __init__(self, productEnum):
        self.ProductEnum = productEnum

        self._newEnumName = ""

    def _getEnumNoCollision(self):
        name = "__enum__"
        idx = 0

        while self.ProductEnum.EnumExists(name):
            idx += 1
            name = f"__enum__{idx}"

        return name

    def ShowEnums(self):
        for enumName in list(self.ProductEnum._enums):
            if imgui.collapsing_header(enumName):

                imgui.push_id(enumName)

                values = self.ProductEnum.GetValues(enumName)

                for value in values:
                    imgui.push_id(value)

                    changed, newValue = imgui.input_text("##Value", value)

                    if changed and imgui.is_item_deactivated_after_edit():
                        if newValue and not self.ProductEnum.Exists(enumName, newValue):
                            self.ProductEnum.RemoveFromEnum(enumName, value)
                            self.ProductEnum.AddToEnum(enumName, newValue)

                    imgui.same_line()

                    if imgui.button("X"):
                        self.ProductEnum.RemoveFromEnum(enumName, value)

                    imgui.pop_id()

                if imgui.button("Add Option"):
                    self.ProductEnum.AddToEnum(enumName, self._getEnumNoCollision())

                imgui.pop_id()

    def Draw(self):
        imgui.push_id("EnumEditor")

        imgui.text("ENUMS:")
        imgui.same_line()

        if imgui.button("+"):
            imgui.open_popup("AddEnumPopup")

        if imgui.begin_popup("AddEnumPopup"):
            changed, self._newEnumName = imgui.input_text("##NewEnum", self._newEnumName)

            if imgui.button("Create") and self._newEnumName != "" and not self.ProductEnum.EnumExists(self._newEnumName):
                self.ProductEnum.NewEnum(self._newEnumName)
                self._newEnumName = ""
                imgui.close_current_popup()

            imgui.end_popup()

        imgui.separator()

        if imgui.begin_child("Enums", size=(400, 300)):
            self.ShowEnums()

        imgui.end_child()

        imgui.pop_id()

class ProductEditor:
    def __init__(self, storageManager, productEnum):
        self.ToBeProducts = []
        self.ProductErrors = {}
        self.StoredProductSearch = ""

        self.StorageManager = storageManager
        self.ProductEnum = productEnum

        self._productTemplate = {
            "UPC": {"Value": "", "Type": "string", "Essential": True}, 
            "Name": {"Value": "", "Type": "string", "Essential": True}, 
        }
        self._productBaseFieldName = "__field__"
        self._productBaseValue = {
            "string": "text",
            "int": 0,
            "float": 0,
            "bool": True,
            "enum": "",
        }

    def _getFieldNoCollision(self, tbProd):
        fieldName = self._productBaseFieldName
        idx = 0
        while fieldName in tbProd:
            idx += 1
            fieldName = f"{fieldName}{idx}"

        return fieldName
    
    def _fieldValue_string(self, data):
        fieldValueChanged, fieldValue = imgui.input_text("##Field value", data["Value"])
        changed = fieldValueChanged and imgui.is_item_deactivated_after_edit()
        if changed:
            data["Value"] = fieldValue

        return changed, fieldValue
        
    def _fieldValue_int(self, data):
        fieldValueChanged, fieldValue = imgui.input_int("##Field value", data["Value"])
        if fieldValueChanged:
            data["Value"] = fieldValue

        return fieldValueChanged, fieldValue

    def _fieldValue_float(self, data):
        fieldValueChanged, fieldValue = imgui.input_float("##Field value", data["Value"])
        if fieldValueChanged:
            data["Value"] = fieldValue

        return fieldValueChanged, fieldValue

    def _fieldValue_bool(self, data):
        fieldValueChanged, fieldValue = imgui.checkbox("##Field value", data["Value"])
        if fieldValueChanged:
            data["Value"] = fieldValue

        return fieldValueChanged, fieldValue
    
    def _fieldValue_enum(self, data):
        current = data["Value"]

        if imgui.begin_combo("##Field value", current):
            for value in self.ProductEnum.Iter(data["Enum"]):
                selected = value == current

                if imgui.selectable(value, selected)[0]:
                    data["Value"] = value

                if selected:
                    imgui.set_item_default_focus()

            imgui.end_combo()

        return False, data["Value"]

    def ValidateProduct(self, tbProd):
        errors = []

        if tbProd["UPC"]["Value"] == "":
            errors.append("UPC is required")

        if tbProd["Name"]["Value"] == "":
            errors.append("Name is required")

        upc = tbProd["UPC"]["Value"]

        if upc in self.StorageManager.Products:
            errors.append("UPC already exists")

        return errors
    
    def BuildProduct(self, tbProd):
        product = Product(tbProd["UPC"]["Value"], tbProd["Name"]["Value"])

        for field, data in tbProd.items():
            if field in ("UPC", "Name"):
                continue

            # FIX PROduCT CLASS
            product.AddAttribute(field, data["Value"], data["Type"] == "enum")

        return product

    def ShowToBeProducts(self):
        for i, tbProd in enumerate(self.ToBeProducts):
            if imgui.collapsing_header(f"[Product] {tbProd["Name"]["Value"] if tbProd["Name"]["Value"] != "" else i}"):
                imgui.push_id(f"ToBeProduct{i}")

                # imgui.text(f"[Product] {tbProd["Name"]["Value"] if tbProd["Name"]["Value"] != "" else i}")

                for key, data in copy.copy(tbProd).items():
                    # Field name input text
                    imgui.push_id(f"Field{key}")

                    imgui.set_next_item_width(em_size(6))
                    fieldKeyChanged, fieldKey = imgui.input_text("Field name", key if not self._productBaseFieldName in key else "", flags=imgui.InputTextFlags_.read_only if data["Essential"] else 0)
                    if fieldKeyChanged and imgui.is_item_deactivated_after_edit():
                        if fieldKey in tbProd:
                            fieldKey = key
                        else:
                            tbProd[fieldKey] = data
                            del tbProd[key]

                        print(tbProd)

                    # Field value input text
                    imgui.same_line()
                    imgui.set_next_item_width(em_size(6))
                    
                    fieldValueFn = getattr(self, f"_fieldValue_{data["Type"]}")
                    changed, _ = fieldValueFn(data)
                    if changed:
                        print(tbProd)

                    # Delete button
                    if not data["Essential"]:
                        imgui.push_style_color(0, ImVec4(1.0, 0.0, 0.0, 1.0))
                        imgui.push_style_color(1, ImVec4(1.0, 0.3, 0.3, 1.0))
                        imgui.push_style_color(2, ImVec4(0.6, 0.0, 0.0, 1.0))

                        imgui.same_line()
                        if imgui.button("X"):
                            # If there's nothing since it was a placeholder then we want to use the original key to delete instead
                            if fieldKey == "":
                                del tbProd[key]
                            else:
                                del tbProd[fieldKey]

                        imgui.pop_style_color(3)

                    imgui.pop_id()

                # Add field button
                if imgui.button("Add Field"):
                    imgui.set_next_window_pos(imgui.get_mouse_pos())
                    imgui.open_popup("AddFieldPopup")

                if imgui.begin_popup("AddFieldPopup"):
                    for type, defaultVal in self._productBaseValue.items():
                        if type == "enum":
                            continue

                        if imgui.selectable(type, False)[0]:
                            tbProd[self._getFieldNoCollision(tbProd)] = {
                                "Value": defaultVal,
                                "Type": type,
                                "Essential": False,
                            }

                    if imgui.begin_menu("enum"):
                        for enumName in self.ProductEnum._enums:

                            if imgui.selectable(enumName, False)[0]:
                                values = self.ProductEnum.GetValues(enumName)

                                tbProd[self._getFieldNoCollision(tbProd)] = {
                                    "Value": values[0] if values else "",
                                    "Type": "enum",
                                    "Enum": enumName,
                                    "Essential": False,
                                }

                        imgui.end_menu()
                    imgui.end_popup()

                imgui.pop_id()


    def Draw(self):
        imgui.push_id("ProductEditor")

        imgui.text("PRODUCTS: ")
        imgui.same_line()
        if imgui.button("+"):
            self.ToBeProducts.append(copy.deepcopy(self._productTemplate))

        imgui.separator()
        if imgui.begin_child("Products", size=(400, 300)):
            self.ShowToBeProducts()

        imgui.end_child()

        imgui.pop_id()
        


class MainApp:
    def __init__(self, storageManager, productEnum):
        self.Filter = imgui.TextFilter()

        self.ProductEditor = ProductEditor(storageManager, productEnum)
        self.EnumEditor = EnumEditor(productEnum)

        self.StorageManager = storageManager

    def Draw(self):
        if imgui.begin_tab_bar("MainTab"):
            opened, visible = imgui.begin_tab_item("Product Editor")
            if opened: 
                self.ProductEditor.Draw()
                self.EnumEditor.Draw()
            
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
        self.MainApp = MainApp(storageManager, productEnum)
        # self.StorageManager = storageManager
        # self.ProductEnum = productEnum

        def gui():
            self.MainApp.Draw()

        hello_imgui.run(gui, window_title="Warehouse Management System")