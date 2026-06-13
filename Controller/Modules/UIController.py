from Packages.imgui import imgui, hello_imgui

selected_idx = 0
items = ["Apple", "Banana", "Cherry"]

def gui():
    global selected_idx
    imgui.text("Choose a fruit:")
    _, selected_idx = imgui.list_box("##fruits", selected_idx, items)
    imgui.text(f"You selected: {items[selected_idx]}")

hello_imgui.run(gui, window_title="Fruit Picker")