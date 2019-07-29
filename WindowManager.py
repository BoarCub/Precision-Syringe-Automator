from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import os
from DataManager import FileImporter
 
 #each class is a window that is being called via the kv file

class MainWindow(Screen):
    pass

class NewRoutineWindow(Screen):
    pass

class NewTaskWindow(Screen):
    pass

class FileChooserWindow(Screen):

    def selectFile(self, *args): #the FileChooser in the kv file produces a *args list of information
        try:
            fileSelected = args[1][0] #this specifies the file path that is stores within *args
        except:
            fileSelected = None
        FileImporter.setPath(fileSelected)

    def getPath(self):
        return os.path.dirname(os.path.realpath(__file__)) + "/Routines" #sets default folder to FileChooser interface

    def openFile(self):
        FileImporter.importFile() #calls method in DataManager which imports file using json
        
    pass

class DisplayFileWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("SyringeInterface.kv") #specifies the kv file in use

class MyMainApp(App):

    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()