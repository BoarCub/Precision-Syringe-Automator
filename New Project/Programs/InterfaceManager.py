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
        
        mode = TaskManager.newTaskActions[str(TaskManager.taskRows.index(button.parent)+1)][0]
        index = str(TaskManager.taskRows.index(button.parent) + 1)
        
        if mode == "Dispense" or mode == "Retrieve" or mode == "Back-and-Forth":
            self.currentPopupValues = [None, None, None]
            self.popup = self.getDefaultPopup(mode, index)
        elif mode == "Recycle":
            self.popup = self.getDoubleValvePopup(mode)
            
    #A callback function that is called when the valve spinner of the popup changes
    def valveSpinnerCallback(self, instance, value):
        try:
            self.currentPopupValues[0] = int(value)
        except:
            self.currentPopupValues[0] = None
        
    #A callback function that is called when volume textinput of the popup changes value
    def volumeTextInputCallback(self, instance, value):
        try:
            self.currentPopupValues[1] = int(value)
        except:
            self.currentPopupValues[1] = None
        
    #A callback function that is called when speed textinput of the popup changes value
    def speedTextInputCallback(self, instance, value):
        try:
            self.currentPopupValues[2] = int(value)
        except:
            self.currentPopupValues[2] = None
            
    #A callback function that is called when time textinput of the popup changes value
    def timeTextInputCallback(self, instance, value):
        try:
            self.currentPopupValues[3] = int(value)
        except:
            self.currentPopupValues[3] = None
            
    #A callback function that is called when the second valve spinner of the popup changes
    def secondValveSpinnerCallback(self, instance, value):
        try:
            self.currentPopupValues[4] = int(value)
        except:
            self.currentPopupValues[4] = None
        
    #A callback function that is called when the confirm button is pressed on the default popup
    def defaultPopupConfirmCallback(self, instance):
        TaskManager.newTaskActions[instance.parent.parent.parent.parent.title[13:]][1] = self.currentPopupValues
        print(TaskManager.newTaskActions)
    
    #Returns a newly generated popup
    def getDefaultPopup(self, mode, index):
            
        popup = Popup(title = "Editing Task " + index,
                      content = FloatLayout(size = self.size),
                      size_hint = (0.5, 0.8))
        
        valve = Spinner(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.75},
            text = "Select Valve",
            values = ('1', '2', '3', '4', '5', '6', '7', '8')
            )
        valve.bind(text = self.valveSpinnerCallback)
        
        volumeInput = TextInput(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.6},
            hint_text = "Volume",
            multiline = False,
            input_filter = 'int'
            )
        volumeInput.bind(text = self.volumeTextInputCallback)
        
        speedInput = TextInput(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.45},
            hint_text = "Speed",
            multiline = False,
            input_filter = 'int'
            )
        speedInput.bind(text = self.speedTextInputCallback)
        
        confirmButton = Button(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.3},
            text = "Confirm"
            )
        confirmButton.bind(on_press = self.defaultPopupConfirmCallback)
        
        popup.content.add_widget(valve)
        popup.content.add_widget(volumeInput)
        popup.content.add_widget(speedInput)
        popup.content.add_widget(confirmButton)
        
        popup.open()
        
        return popup
    
        #Returns a newly generated popup
    def getDoubleValvePopup(self, mode):
            
        popup = Popup(title = mode,
                      content = FloatLayout(size = self.size),
                      size_hint = (0.5, 0.8))
        
        outputValve = Spinner(
            size_hint = (0.4, 0.1),
            pos_hint = {'center_x': 0.25, 'center_y': 0.75},
            text = "Select Output Valve",
            values = ('1', '2', '3', '4', '5', '6', '7', '8')
            )
        
        bypassValve = Spinner(
            size_hint = (0.4, 0.1),
            pos_hint = {'center_x': 0.75, 'center_y': 0.75},
            text = "Select Bypass Valve",
            values = ('1', '2', '3', '4', '5', '6', '7', '8')
            )
        
        volumeInput = TextInput(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.6},
            hint_text = "Volume",
            multiline = False,
            input_filter = 'int'
            )
        
        speedInput = TextInput(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.45},
            hint_text = "Speed",
            multiline = False,
            input_filter = 'int'
            )
        
        confirmButton = Button(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.3},
            text = "Confirm"
            )
        
        popup.content.add_widget(outputValve)
        popup.content.add_widget(bypassValve)
        popup.content.add_widget(volumeInput)
        popup.content.add_widget(speedInput)
        popup.content.add_widget(confirmButton)
        
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