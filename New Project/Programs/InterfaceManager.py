import os

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

from TaskManager import TaskManager
from FileManager import *

# InterfaceManager acts as a container for all of the Screens in the app
class InterfaceManager(ScreenManager):
    pass


# The container for the StartScreen Screen
class StartScreen(Screen):
    pass


# The container for the RoutineCreator Screen
class RoutineCreatorScreen(Screen):
    pass

class SaveFileScreen(Screen):
    def save(self, path, filename):
        FileManager.writeFile(path, filename)

    def getPath(self):
        return FileManagershortenFilePath(os.path.dirname(os.path.realpath(__file__))) + "/Routines"
#Allows the reader to load a previously saved file and use that
class PreviousFileScreen(Screen):
    def getPath(self):
        return  FileManager.shortenFilePath(os.path.dirname(os.path.realpath(__file__)))+ "/Routines"
    #recieves the file path from the file chooser
    def selectFile(self, *args):
        print("File selected: ", args[1][0])
        FileManager.setPath(args[1][0])
    
    #signals the widgets to update based on the selected file
    def updateDisplay(self, object):
        print("file being imported", FileManager.importFile())
        self.updateWidgets(FileManager.parseString(FileManager.importFile()), object)
    
    #updates widgets based on a list of commands and their values to display
    def updateWidgets(self, actions_list, object):
        #only works nothing has previously been displayed on the screen
        if(FileManager.displayed_actions != None):
            for action in FileManager.displayed_actions:
                object.ids.display_box.remove_widget(action)
        
        #after displaying, it clears the cache to prepare for the nexy display
        FileManager.displayed_actions = []
        
        #for every action in the list of actions
        for small_list in actions_list:
            placeholderLayout = BoxLayout()
            
            #for every item in each action (ex: Execute Command Buffer, or 83)
            for element in small_list:
                placeholderLayout.add_widget(Label(text=str(element)))
            
            #add it to the list of displayed_actions just so we know what the last thing displayed was at any given time
            FileManager.displayed_actions.append(placeholderLayout)
            
            #add the widget to the displayfilescreen's box layout (id: display_box)
            object.ids.display_box.add_widget(placeholderLayout)
    
    
#displays a file based on what is loaded from previous file screen   
class DisplayFileScreen(Screen):
    pass


#Processes the execution visuals for the user
class ExecuteFileScreen(Screen):
    pass
# Loads the .kv file needed
kv = Builder.load_file("Interface.kv")


# Builds the app
class MainApp(App):

    def build(self):
        return kv


# Main Function which runs the app
if __name__ == "__main__":
    
    MainApp().run()