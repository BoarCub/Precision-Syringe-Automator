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

    def updateWidgets(bigList):
        
        for smallList in bigList:
            
            placeholderBoxLayout = BoxLayout()
            
            for element in smallList:
                placeholderBoxLayout.add_widget(Label(text=element))
                
            self.ids.display_box.add_widget(placeholderBoxLayout)

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