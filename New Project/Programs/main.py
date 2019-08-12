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

class SaveFileScreen(Screen):
    def save(self, path, filename):
        FileManager.writeFile(path, filename)

    def getPath(self):
        return FileManager.shortenFilePath(os.path.dirname(os.path.realpath(__file__))) + "/Routines"
    
    
#The container for the RoutineCreator Screen
class RoutineCreatorScreen(Screen):
    
    #Super Init
    def __init__(self, **kwargs):
        super(RoutineCreatorScreen, self).__init__(**kwargs)
        self.deleteToggled = False
    
    def toggleDelete(self, button):
        self.deleteToggled = not self.deleteToggled
        
        if self.deleteToggled:
            button.text = "Cancel"
            self.setDetailsButtonColor((1, 0, 0, 1))
        else:
            button.text = "Delete Action"
            self.setDetailsButtonColor((1, 1, 1, 1))
    
    def setDetailsButtonColor(self, color):
        for layout in TaskManager.taskRows:
            for widget in layout.children:
                if widget.id == "details_button":
                    widget.background_color = color
                    break
    
    def resetTask(self):
        while len(TaskManager.newTaskActions) > 0:
            self.deleteAction(1)
            
        if self.deleteToggled:
            self.toggleDelete(self.delete_button)
    
    def deleteAction(self, index):
        layoutToDelete = TaskManager.taskRows[index-1]
        TaskManager.deleteAction(index)
        self.actions_layout.remove_widget(layoutToDelete)
        self.toggleDelete(self.delete_button)
    
    def replaceTask(self, taskDictionary):
        self.resetTask()
        
        for i in range (1, len(taskDictionary) + 1):
            layout = self.addEmptyAction()
            
            for widget in layout.children:
                if widget.id == "mode_spinner":
                    widget.text = taskDictionary[str(i)][0]
                    
            for widget in layout.children:
                if widget.id == "details_button":
                    widget.text = TaskManager.getDetails(taskDictionary[str(i)])
                    
            TaskManager.newTaskActions[str(i)][1] = taskDictionary[str(i)][1] 
    
    def saveFileScreen(self, nextScreen, currentScreen):
        if TaskManager.checkNone():
            return nextScreen
        else:
            self.notifyPopup = Popup(title = "Warning",
                                     content = FloatLayout(size = self.size),
                                     size_hint = (0.5, 0.8))
            
            okayLabel = Label(
                size_hint = (0.5, 0.1),
                pos_hint = {'center_x': 0.5, 'center_y': 0.7},
                text = "Some Actions Are\nIncomplete",
                halign = 'center',
                font_size = "20sp"
            )
            
            okayButton = Button(
                size_hint = (0.5, 0.1),
                pos_hint = {'center_x': 0.5, 'center_y': 0.3},
                text = "Okay"
            )
            okayButton.bind(on_press = self.closeNotifyPopup)
            
            self.notifyPopup.content.add_widget(okayLabel)
            self.notifyPopup.content.add_widget(okayButton)
            
            self.notifyPopup.open()
            
            return currentScreen
            
    def updateWidgetText(self, widget, parameterIndex):
        widget.text = str(self.currentPopupValues[parameterIndex])
    
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
        
        return layout
        
    #A callback function that is called when the text value of a mode spinner changes
    def updateModeSpinner(self, spinner, value):
        TaskManager.newTaskActions[str(TaskManager.taskRows.index(spinner.parent)+1)][0] = value
        TaskManager.newTaskActions[str(TaskManager.taskRows.index(spinner.parent)+1)][1] = None
        
        for widget in spinner.parent.children:
            if widget.id == "details_button":
                widget.disabled = False
                widget.text = "Add Details"
                return
            
    #A callback function that is called when the edit button is pressed
    def editButtonCallback(self, button):
        
        if(self.deleteToggled):
            self.deleteAction(TaskManager.taskRows.index(button.parent)+1)
        else:
            self.openDetailEditor(button)
            
    #Called to initialize popup for detail editor
    def openDetailEditor(self, button):
        mode = TaskManager.newTaskActions[str(TaskManager.taskRows.index(button.parent)+1)][0]
        index = str(TaskManager.taskRows.index(button.parent) + 1)
        
        if mode == "Dispense" or mode == "Retrieve":
            self.currentPopupValues = self.getCurrentValues([None, None, None], index)
            self.popup = self.getDefaultPopup(mode, index)
        elif mode == "Back-and-Forth":
            self.currentPopupValues = self.getCurrentValues([None, None, None, None], index)
            self.popup = self.getTimePopup(mode, index)
        elif mode == "Recycle":
            self.currentPopupValues = self.getCurrentValues([None, None, None, None, None], index)
            self.popup = self.getTimeAndExtraValvePopup(mode, index)
            
    def getCurrentValues(self, alternateValues, index):
        if TaskManager.newTaskActions[str(index)][1] == None:
            return alternateValues
        else:
            return TaskManager.newTaskActions[str(index)][1]
            
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
        
        index = instance.parent.parent.parent.parent.title[13:]
        
        if(TaskManager.checkParameters([TaskManager.newTaskActions[index][0], self.currentPopupValues])):
            TaskManager.newTaskActions[index][1] = self.currentPopupValues
            
            self.popup.dismiss()
            
            for widget in TaskManager.taskRows[int(index)-1].children:
                if widget.id == "details_button":
                    widget.text = TaskManager.getDetails(TaskManager.newTaskActions[index])
        else:
            self.notifyPopup = Popup(title = "Warning",
                                     content = FloatLayout(size = self.size),
                                     size_hint = (0.5, 0.8))
            
            okayLabel = Label(
                size_hint = (0.5, 0.1),
                pos_hint = {'center_x': 0.5, 'center_y': 0.7},
                text = "Your Input Was\nInvalid",
                halign = 'center',
                font_size = "20sp"
            )
            
            okayButton = Button(
                size_hint = (0.5, 0.1),
                pos_hint = {'center_x': 0.5, 'center_y': 0.3},
                text = "Okay"
            )
            okayButton.bind(on_press = self.closeNotifyPopup)
            
            self.notifyPopup.content.add_widget(okayLabel)
            self.notifyPopup.content.add_widget(okayButton)
            
            self.notifyPopup.open()
    
    #Callback function that closes the notify popup
    def closeNotifyPopup(self, instance):
        self.notifyPopup.dismiss()
    
    #Returns a newly generated popup
    def getDefaultPopup(self, mode, index):
        
        currentPopupValuesIsEmpty = True
        for value in self.currentPopupValues:
            if value != None:
                currentPopupValuesIsEmpty = False
        
        popup = Popup(title = "Editing Task " + index,
                      content = FloatLayout(size = self.size),
                      size_hint = (0.5, 0.8))
        
        valve = Spinner(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.75},
            text = "Select Valve",
            values = ('1', '2', '3', '4', '5', '6', '7', '8')
            )
        if not currentPopupValuesIsEmpty:
            self.updateWidgetText(valve, 0)
        valve.bind(text = self.valveSpinnerCallback)
        
        valveLabel = Label(
            pos_hint = {"center_x": 0.5, "center_y": 0.85},
            text = "Valve:",
            halign = "center"
            )
        
        volumeInput = TextInput(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.6},
            hint_text = "Volume",
            multiline = False,
            input_filter = 'int'
            )
        if not currentPopupValuesIsEmpty:
            self.updateWidgetText(volumeInput, 1)
        volumeInput.bind(text = self.volumeTextInputCallback)
        
        speedInput = TextInput(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.45},
            hint_text = "Speed",
            multiline = False,
            input_filter = 'int'
            )
        if not currentPopupValuesIsEmpty:
            self.updateWidgetText(speedInput, 2)
        speedInput.bind(text = self.speedTextInputCallback)
        
        confirmButton = Button(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.3},
            text = "Confirm"
            )
        confirmButton.bind(on_press = self.defaultPopupConfirmCallback)
        
        popup.content.add_widget(valveLabel)
        popup.content.add_widget(valve)
        popup.content.add_widget(volumeInput)
        popup.content.add_widget(speedInput)
        popup.content.add_widget(confirmButton)
        
        popup.open()
        
        return popup
    
    #Returns a newly generated popup with an added widget for time
    def getTimePopup(self, mode, index):
        
        currentPopupValuesIsEmpty = True
        for value in self.currentPopupValues:
            if value != None:
                currentPopupValuesIsEmpty = False
        
        popup = Popup(title = "Editing Task " + index,
                      content = FloatLayout(size = self.size),
                      size_hint = (0.5, 0.8))
        
        valve = Spinner(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.75},
            text = "Select Valve",
            values = ('1', '2', '3', '4', '5', '6', '7', '8')
            )
        if not currentPopupValuesIsEmpty:
            self.updateWidgetText(valve, 0)
        valve.bind(text = self.valveSpinnerCallback)
        
        valveLabel = Label(
            pos_hint = {"center_x": 0.5, "center_y": 0.85},
            text = "Valve:",
            halign = "center"
            )
        
        volumeInput = TextInput(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.6},
            hint_text = "Volume",
            multiline = False,
            input_filter = 'int'
            )
        if not currentPopupValuesIsEmpty:
            self.updateWidgetText(volumeInput, 1)
        volumeInput.bind(text = self.volumeTextInputCallback)
        
        speedInput = TextInput(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.45},
            hint_text = "Speed",
            multiline = False,
            input_filter = 'int'
            )
        if not currentPopupValuesIsEmpty:
            self.updateWidgetText(speedInput, 2)
        speedInput.bind(text = self.speedTextInputCallback)
        
        timeInput = TextInput(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.3},
            hint_text = "Time",
            multiline = False,
            input_filter = 'int'
            )
        if not currentPopupValuesIsEmpty:
            self.updateWidgetText(timeInput, 3)
        timeInput.bind(text = self.timeTextInputCallback)
        
        confirmButton = Button(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.15},
            text = "Confirm"
            )
        confirmButton.bind(on_press = self.defaultPopupConfirmCallback)
        
        popup.content.add_widget(valveLabel)
        popup.content.add_widget(valve)
        popup.content.add_widget(volumeInput)
        popup.content.add_widget(speedInput)
        popup.content.add_widget(timeInput)
        popup.content.add_widget(confirmButton)
        
        popup.open()
        
        return popup
    
    #Returns a newly generated popup with an added widget for time
    def getTimeAndExtraValvePopup(self, mode, index):
        
        currentPopupValuesIsEmpty = True
        for value in self.currentPopupValues:
            if value != None:
                currentPopupValuesIsEmpty = False
        
        popup = Popup(title = "Editing Task " + index,
                      content = FloatLayout(size = self.size),
                      size_hint = (0.5, 0.8))
        
        valve = Spinner(
            size_hint = (0.45, 0.1),
            pos_hint = {'center_x': 0.25, 'center_y': 0.75},
            text = "Select Valve",
            values = ('1', '2', '3', '4', '5', '6', '7', '8')
            )
        if not currentPopupValuesIsEmpty:
            self.updateWidgetText(valve, 0)
        valve.bind(text = self.valveSpinnerCallback)
        
        extraValve = Spinner(
            size_hint = (0.45, 0.1),
            pos_hint = {'center_x': 0.75, 'center_y': 0.75},
            text = "Select Valve",
            values = ('1', '2', '3', '4', '5', '6', '7', '8')
            )
        if not currentPopupValuesIsEmpty:
            self.updateWidgetText(extraValve, 4)
        extraValve.bind(text = self.secondValveSpinnerCallback)
        
        valveLabel = Label(
            pos_hint = {"center_x": 0.25, "center_y": 0.85},
            text = "Main Valve:",
            halign = "center"
            )
        
        extraValveLabel = Label(
            pos_hint = {"center_x": 0.75, "center_y": 0.85},
            text = "Bypass Valve:",
            halign = "center"
            )
        
        volumeInput = TextInput(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.6},
            hint_text = "Volume",
            multiline = False,
            input_filter = 'int'
            )
        if not currentPopupValuesIsEmpty:
            self.updateWidgetText(volumeInput, 1)
        volumeInput.bind(text = self.volumeTextInputCallback)
        
        speedInput = TextInput(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.45},
            hint_text = "Speed",
            multiline = False,
            input_filter = 'int'
            )
        if not currentPopupValuesIsEmpty:
            self.updateWidgetText(speedInput, 2)
        speedInput.bind(text = self.speedTextInputCallback)
        
        timeInput = TextInput(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.3},
            hint_text = "Time",
            multiline = False,
            input_filter = 'int'
            )
        if not currentPopupValuesIsEmpty:
            self.updateWidgetText(timeInput, 3)
        timeInput.bind(text = self.timeTextInputCallback)
        
        confirmButton = Button(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.15},
            text = "Confirm"
            )
        confirmButton.bind(on_press = self.defaultPopupConfirmCallback)
        
        popup.content.add_widget(valveLabel)
        popup.content.add_widget(extraValveLabel)
        popup.content.add_widget(valve)
        popup.content.add_widget(extraValve)
        popup.content.add_widget(volumeInput)
        popup.content.add_widget(speedInput)
        popup.content.add_widget(timeInput)
        popup.content.add_widget(confirmButton)
        
        popup.open()
        
        return popup
        
        
#Allows the reader to load a previously saved file and use that
class PreviousFileScreen(Screen):
    def getPath(self):
        return  FileManager.shortenFilePath(os.path.dirname(os.path.realpath(__file__)))+ "/Routines"
    #recieves the file path from the file chooser
    def selectFile(self, *args):
        try:
            print("File selected: ", args[1][0])
            FileManager.setPath(args[1][0])
        except:
            pass
    
    #signals the widgets to update based on the selected file
    def updateDisplay(self, object):
        print("file being imported", FileManager.importFile())
        current_dict = FileManager.importFile()
        if current_dict!= None:
            object.replaceTask(current_dict)


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