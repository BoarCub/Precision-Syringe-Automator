from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
import os
from DataManager import FileImporter
from TaskCreator import *

from SerialManager import *

 #each class is a window that is being called via the kv file

class MainWindow(Screen):
    pass

class NewRoutineWindow(Screen):
    pass

class NewTaskWindow(Screen):
    def clickMode(self, value):
        taskcreator_object.takeMode(value)
    def getUserCommands(self):
        return FileImporter.userCommands()
    def clickAction(self, value):
        taskcreator_object.takeAction(value)
    def clickNum(self, value):
        taskcreator_object.takeNum(value)
class ExecuteFileWindow(Screen):
    
    def startLoop(self):
        serial_object.startQueryUpdate(self.ids.queryLabel)
        
    def stopLoop(self):
        serial_object.stopQueryUpdate()
    
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
        
    def updateDisplay(self, object):
        
        self.updateWidgets(FileImporter.parseImportedString(FileImporter.importFile()), object)
    
    def updateWidgets(self, bigList, object):
        
        if(FileImporter.displayedActions != None):
            for action in FileImporter.displayedActions:
                object.ids.display_box.remove_widget(action)
        
        FileImporter.displayedActions = []
        
        for smallList in bigList:
            placeholderLayout = BoxLayout()
            
            for element in smallList:
                placeholderLayout.add_widget(Label(text=element))
            
            FileImporter.displayedActions.append(placeholderLayout)
            
            object.ids.display_box.add_widget(placeholderLayout)
        
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