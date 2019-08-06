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


#The container for the RoutineCreator Screen
class RoutineCreatorScreen(Screen):
    
    #Creates an empty action and adds it to the task and screen
    def addEmptyAction(self):
        
        layout = FloatLayout(
            )
        
        taskLabel = Label(
            id = "task_label",
            text = str(len(TaskManager.newTaskActions)+1),
            size_hint = (0.15, 1),
            pos_hint = {'center_x': 0.08, 'center_y': 0.5}
            )
        
        spinner = Spinner(text = "Choose Mode",
                          id = "mode_spinner",
                          values = ('Dispense', 'Retrieve', 'Back-and-Forth', 'Recycle'),
                          size_hint = (0.3, 1),
                          pos_hint = {'center_x': 0.3, 'center_y': 0.5}
                          )
        
        spinner.bind(text = self.updateModeSpinner)
        
        detailsButton = Button(
            id = "details_button",
            text = "Choose a Mode First",
            size_hint = (0.5, 1),
            pos_hint = {'center_x': 0.725, 'center_y': 0.5},
            disabled = True
            )
        
        detailsButton.bind(on_press = self.editButtonCallback)
        
        layout.add_widget(taskLabel)
        layout.add_widget(spinner)
        layout.add_widget(detailsButton)
        
        TaskManager.taskRows.append(layout)
        
        self.actions_layout.add_widget(layout)
        
        TaskManager.newTaskActions.update({str(len(TaskManager.newTaskActions)+1): [None, None]})
        
    #A callback function that is called when the text value of a mode spinner changes
    def updateModeSpinner(self, spinner, value):
        
        TaskManager.newTaskActions[str(TaskManager.taskRows.index(spinner.parent)+1)][0] = value
        
        for widget in spinner.parent.children:
            if widget.id == "details_button":
                widget.disabled = False
                widget.text = "Add Details"
                return
            
    #A callback function that is called when the edit button is pressed
    def editButtonCallback(self, button):
        
        self.popup = self.getPopup(TaskManager.newTaskActions[str(TaskManager.taskRows.index(button.parent)+1)][0])
            
    #Returns a popup depending on what mode is given
    def getPopup(self, mode):
        
        if mode == "Dispense":
            
            popup = Popup(title = mode,
                          content = FloatLayout(),
                          size_hint = (0.8, 0.8))
            
            popup.open()
            
            return popup
        
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
                placeholderLayout.add_widget(Label(text=element))
            
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