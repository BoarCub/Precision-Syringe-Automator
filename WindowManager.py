from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.dropdown import DropDown
import os
class MainWindow(Screen):
    pass

class NewRoutineWindow(Screen):
    pass

class NewTaskWindow(Screen):
    pass

class FileChooserWindow(Screen):
    
    def __init__(self):
        print("yo")
    
    def selectFile(self, *args):
        try:
            self.fileSelected = args[1][0]
        except:
            self.fileSelected = None
    
    def getPath(self):
        return os.path.dirname(os.path.realpath(__file__)) + "/Routines"
    
    def openFile(self):
        if self.fileSelected == None:
            print("No file is currently selected")
        else:
            print("Opening " + fileSelected)
    
    pass

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")

class MyMainApp(App):
    
    def build(self):
        return kv
    
    def selectPath(self, path):
        print(path)
    
if __name__ == "__main__":
    MyMainApp().run()