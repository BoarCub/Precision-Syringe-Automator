from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.dropdown import DropDown
import os
from DataManager import FileImporter
class MainWindow(Screen):
    pass

class NewRoutineWindow(Screen):
    pass

class NewTaskWindow(Screen):
    pass

class FileChooserWindow(Screen):
    
    def selectFile(self, *args):
        try:
            fileSelected = args[1][0]
        except:
            fileSelected = None
        FileImporter.setPath(fileSelected)
    
    def getPath(self):
        return os.path.dirname(os.path.realpath(__file__)) + "/Routines"
    
    def openFile(self):
        FileImporter.importFile()
    
    pass

class DisplayFileWindow(Screen):
    
    def openFile(self):
        imported = FileImporter.importFile()
        
        if(imported == None):
            return ""
        else:
            return imported
    
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