from Packages.imgui.imgui_bundle import imgui, hello_imgui, em_to_vec2, em_size
from typing import TYPE_CHECKING

from Utils import CustomInput
from Utils.Signal import Signal


selected_idx = 0

class MainApp:
    def __init__(self):
        self.filter = imgui.TextFilter()

    def draw(self):
        self.filter.draw('Search ("incl,-excl") ("error")', em_size(25))
        

class Init:
    def __init__(self, CONTROLLERS):
        global Module
        self._CONTROLLERS = CONTROLLERS
        Module = self

        self.MainApp = MainApp()
            
    def start(self):
        def gui():
            self.MainApp.draw()

        hello_imgui.run(gui, window_title="Warehouse Management System")