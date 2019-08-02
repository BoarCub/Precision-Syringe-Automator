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
    
    def addAction(self):
        index = len(TaskManager.newTaskActions) + 1
        TaskManager.newTaskActions.update( {str(index): [None, None, None, None, None]} )
        
        print(TaskManager.newTaskActions)
        self.updateScreen()
                
    def updateScreen(self):
        if( len(TaskManager.newTaskActions) <= len(self.ids.actions_box.children) ):
             print("Available Space")
             
             for index in range(1, len(TaskManager.newTaskActions)+1):
                 print(index)
                 self.displayAction(index, index, TaskManager.newTaskActions[str(index)])
             
        else:
            print("No available space")
    
    def displayAction(self, position, index, list):
        
        layout = self.ids.actions_box.children[len(self.ids.actions_box.children) - position]
        
        for widget in TaskManager.previousWidgets[position-1]:
            layout.remove_widget(widget)
        
        TaskManager.previousWidgets[position-1] = []
        
        indexLabel = Label(text = str(index))
        inputSpinner = self.formatSpinner(self.generateValveSpinner(True), list[0])
        outputSpinner = self.formatSpinner(self.generateValveSpinner(False), list[1])
        modeSpinner = self.formatSpinner(self.generateModeSpinner(), list[2])
        
        layout.add_widget(indexLabel)
        layout.add_widget(inputSpinner)
        layout.add_widget(outputSpinner)
        layout.add_widget(modeSpinner)
        
        TaskManager.previousWidgets[position-1].append(indexLabel)
        TaskManager.previousWidgets[position-1].append(inputSpinner)
        TaskManager.previousWidgets[position-1].append(outputSpinner)
        TaskManager.previousWidgets[position-1].append(modeSpinner)
        
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
    
    def generateModeSpinner(self):
        spinner = Spinner(
            text = 'Empty',
            values = ('Time', 'Volume')
            )
        
        spinner.id = 'mode'
        
        spinner.bind(text = self.updateSpinnerValues)
        
        return spinner
    
    def formatSpinner(self, spinner, value):
        if(value != None):
            spinner.text = str(value)
        return spinner
    
    def updateSpinnerValues(self, spinner, text):
        print("Text: " + text + " " + spinner.id)

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
        self.updateWidgets(FileManager.parseString(FileManager.importFile()))
    
    #updates widgets based on a list of commands and their values to display
    def updateWidgets(self, actions_list, object):
        
        if(FileManager.displayed_actions != None):
            for action in FileManager.displayed_actions:
                object.ids.display_box.remove_widget(action)
        
        FileManager.displayed_actions = []
        
        for smallList in actions_list:
            placeholderLayout = BoxLayout()
            
            for element in smallList:
                placeholderLayout.add_widget(Label(text=element))
            
            FileManager.displayed_actions.append(placeholderLayout)
            
            object.ids.display_box.add_widget(placeholderLayout)
    
    
#displays a file based on what is loaded from previous file screen   
class DisplayFileScreen(Screen):
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