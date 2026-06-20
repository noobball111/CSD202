from Services import UIService
from Services.FileLoader import FileLoader

DEFAULT_SAVE_FILE = "Data/Data.txt"

UIService.Init()
FileLoader = FileLoader()

FileLoader.Load(None or DEFAULT_SAVE_FILE)

print(FileLoader.Loaded)