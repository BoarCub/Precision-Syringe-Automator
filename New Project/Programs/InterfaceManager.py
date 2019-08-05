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
    
    # Adds am empty action to the task
    def addAction(self):
        index = len(TaskManager.newTaskActions) + 1
        TaskManager.newTaskActions.update( {str(index): [None, None, None, None, None]} )
        
        print(TaskManager.newTaskActions)
        self.updateScreen()
    
    # Updates the widgets on the screen with any changes to the task
    def updateScreen(self):
        if( len(TaskManager.newTaskActions) <= len(self.ids.actions_box.children) ):
             print("Available Space")
             
             for index in range(1, len(TaskManager.newTaskActions)+1):
                 print(index)
                 self.displayAction(index, index, TaskManager.newTaskActions[str(index)])
             
        else:
            print("No available space")
    
    # Displays an action on the screen
    # position represents the position on the screen that the action is to be displayed, starting with 1
    # index represents the step number of the action in the task, starting with 1
    # list is a list represents the different properties of the task: [input valve, output valve, mode, value, speed]. This follows the same format as in TaskManager.newTaskActions
    def displayAction(self, position, index, list):
        
        layout = self.ids.actions_box.children[len(self.ids.actions_box.children) - position]
        
        for widget in TaskManager.previousWidgets[position-1]:
            layout.remove_widget(widget)
        
        TaskManager.previousWidgets[position-1] = []
        
        indexLabel = Label(text = str(index))
        inputSpinner = self.formatSpinner(self.generateValveSpinner(True), list[0])
        outputSpinner = self.formatSpinner(self.generateValveSpinner(False), list[1])
        modeSpinner = self.formatSpinner(self.generateModeSpinner(), list[2])
        valueInput = self.formatTextInput(self.generateValueText(), list[3])
        speedInput = self.formatTextInput(self.generateSpeedText(), list[4])
        
        layout.add_widget(indexLabel)
        layout.add_widget(inputSpinner)
        layout.add_widget(outputSpinner)
        layout.add_widget(modeSpinner)
        layout.add_widget(valueInput)
        layout.add_widget(speedInput)
        
        TaskManager.previousWidgets[position-1].append(indexLabel)
        TaskManager.previousWidgets[position-1].append(inputSpinner)
        TaskManager.previousWidgets[position-1].append(outputSpinner)
        TaskManager.previousWidgets[position-1].append(modeSpinner)
        TaskManager.previousWidgets[position-1].append(valueInput)
        TaskManager.previousWidgets[position-1].append(speedInput)
        
    # Returns a new Spinner, representing the valve chosen. isInput is a boolean representing whether the valve is an input valve. Otherwise, the valve is an output valve
    def generateValveSpinner(self, isInput):
        spinner = Spinner(
            text = 'Empty',
            values = ('1', '2', '3', '4', '5', '6', '7', '8')
            )
        
        if isInput:
            spinner.id = 'input'
        else:
            spinner.id = 'output'
        
        spinner.bind(text = self.updateSpinnerValues)
        
        return spinner
  
    # Returns a new Spinner, representing the mode chosen (either time or volume)
    def generateModeSpinner(self):
        spinner = Spinner(
            text = 'Empty',
            values = ('Time', 'Volume')
            )
        
        spinner.id = 'mode'
        
        spinner.bind(text = self.updateSpinnerValues)
        
        return spinner
    
    # Returns a new TextInput, representing the value chosen (time or volume)
    def generateValueText(self):
        text = TextInput(
            id = 'value_text',
            hint_text = 'Value',
            multiline = False,
            input_filter = 'int'
            )
        
        text.bind(text = self.updateTextValues)
        
        return text
    
    # Returns a new TextInput, representing the speed chosen
    def generateSpeedText(self):
        text = TextInput(
            id = 'speed_text',
            hint_text = 'Speed',
            multiline = False,
            input_filter = 'int'
            )
        
        text.bind(text = self.updateTextValues)
        
        return text
    
    # Sets the text of the spinner based on a value given
    def formatSpinner(self, spinner, value):
        if(value != None):
            spinner.text = str(value)
        return spinner
    
    # Sets the text of the TextInput based on a value given
    def formatTextInput(self, textInput, value):
        if(value != None):
            textInput.text = value
        return textInput
    
    def updateTextValues(self, textbox, text):
        
        if(textbox.id == 'value_text'):
            index = 3
        else:
            index = 4
            
        try:
            TaskManager.newTaskActions[ str(self.widgetIndexToTaskIndex(self.findIndexOfParent(textbox))) ][index] = text
        except:
            pass
    
    # This function updates newTaskActions with any new values in the spinners
    def updateSpinnerValues(self, spinner, text):
        
        try:
            text = int(text)
        except:
            pass
        
        if(spinner.id == 'input'):
            index = 0
        elif(spinner.id == 'output'):
            index = 1
        else:
            index = 2
        try:
            TaskManager.newTaskActions[ str(self.widgetIndexToTaskIndex(self.findIndexOfParent(spinner))) ][index] = text
        except:
            pass
        
    def findIndexOfParent(self, widget):
        return self.ids.actions_box.children.index(widget.parent)
    
    def widgetIndexToTaskIndex(self, index):
        return len(self.ids.actions_box.children)-index
        

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