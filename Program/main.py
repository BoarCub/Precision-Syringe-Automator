import os

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout

from TaskManager import TaskManager
from FileManager import *

from SerialManager import *

# InterfaceManager acts as a container for all of the Screens in the app
class InterfaceManager(ScreenManager):
    pass


# The container for the StartScreen Screen
class StartScreen(Screen):
    pass


# The container for the SaveFile Screen
class SaveFileScreen(Screen):
    
    # Takes a parameter of path, which is the path the file will be saved to
    # Takes the parameter filename, which will be the name of the file
    # Saves the current task to that file
    def save(self, path, filename):
        FileManager.writeFile(path, filename)
        self.refresh()

    # Returns the path of the Tasks folder, which stores all of the saved Tasks
    def getPath(self):
        return FileManager.shortenFilePath(os.path.dirname(os.path.realpath(__file__))) + "/Tasks"
    
    # Refreshes the filechooser so that new files are displayed
    def refresh(self):
        self.filechooser._update_files()
    
    
# The container for the TaskCreator Screen
class TaskCreatorScreen(Screen):
    
    # Super Init (Allows for the initialization of class variables
    def __init__(self, **kwargs):
        super(TaskCreatorScreen, self).__init__(**kwargs)
        self.deleteToggled = False # A boolean representing whether delete mode is toggled
    
    # Toggles whether "deleteToggled" is toggled. This value determines whether the detail buttons are in edit mode or delete mode.
    def toggleDelete(self):
        self.deleteToggled = not self.deleteToggled # Toggles delete
        
        if self.deleteToggled: # Delete is active
            self.delete_button.text = "Cancel" # Changes Delete Button text to Cancel
            self.setDetailsButtonColor((1, 0, 0, 1)) # Changes Detail Buttons to red in color
        else: # Delete is inactive
            self.delete_button.text = "Delete Action" # Changes Delete Button text to Delete Action
            self.setDetailsButtonColor((1, 1, 1, 1)) # Changes back color of Detail Buttons to white/gray
    
    # Sets the color of all detail buttons to the color given in the parameter, which is a tuple in the following format: (R, G, B, A)
    def setDetailsButtonColor(self, color):
        for layout in TaskManager.taskRows:
            for widget in layout.children: # Searches for the Detail Button in each layout
                if widget.id == "details_button":
                    widget.background_color = color # Sets the color of Details Button to the parameter
                    break
    
    # Resets the task by deleting all actions in the task
    def resetTask(self):
        while len(TaskManager.newTaskActions) > 0: # Deletes actions at the first index of the task until no actions are left
            self.deleteAction(1)
            
        if self.deleteToggled: # Makes sure delete is untoggled
            self.toggleDelete()
    
    # Deletes the action at the given index corresponding to TaskManager.newTaskActions, starting at 1
    def deleteAction(self, index):
        layoutToDelete = TaskManager.taskRows[index-1] # Gets the layout representing the action
        TaskManager.deleteAction(index) # Deletes the action from the task
        self.actions_layout.remove_widget(layoutToDelete) # Removes the layout representing the action for the scrollable GridLayout
        self.toggleDelete() # Toggled delete
    
    #Replaces all the actions in the task with those in the parameter, given as a dictionary in the same format as TaskManager.newTaskActions
    def replaceTask(self, taskDictionary):
        self.resetTask() # Resets the task so that the task is empty to begin with
        
        for i in range (1, len(taskDictionary) + 1): # Iterates through each action in the given dictionary
            layout = self.addEmptyAction() # An empty action is created
            
            # Sets the value of the mode spinner based on value in the taskDictionary
            for widget in layout.children:
                if widget.id == "mode_spinner":
                    widget.text = taskDictionary[str(i)][0]
                    
            # Sets the value of the detail button to description of the action
            for widget in layout.children:
                if widget.id == "details_button":
                    widget.text = TaskManager.getDetails(taskDictionary[str(i)])
                    
            # Sets the parameters in the running task dictionary (Valve, Volume, Speed) to the ones in the action in the parameter
            TaskManager.newTaskActions[str(i)][1] = taskDictionary[str(i)][1] 
    
    #Checks if the task is ready to save
    #If the task is ready to save, the next screen is opened
    #Otherwise, a popup is opened that tells the user "Some Actions are Incomplete"
    def saveFileScreen(self, nextScreen, currentScreen):
        
        # Whether the task given extends the syringe out of range (less than 0 or greater than 3000)
        # Equal to False if within bounds or a string representing the error message if out of bounds
        outOfBounds = TaskManager.checkOutOfBounds()
        
        # Returns True if none of actions are empty and none of the parameters of the action are empty
        checkNone = TaskManager.checkNone()
        
        # No issues, the task and all of its actions are valid
        if checkNone and outOfBounds == False:
            return nextScreen # Returns the nextScreen to continue to
        else: #There are some issues with the task, displaying error to the user through a notification
            self.customPopup = Popup(title = "Warning",
                                     content = FloatLayout(size = self.size),
                                     size_hint = (0.5, 0.8))
            
            #labelText is the string that will be displayed to the user
            if not checkNone: #One or more actions are empty or have empty parameters
                labelText = "Some Actions Are\nIncomplete"
            else: #Since no actions are empty, the error must be that the pump goes out of bounds
                labelText = outOfBounds
            
            # Creates a label that will display the message to the user
            messageLabel = Label(
                size_hint = (0.5, 0.1),
                pos_hint = {'center_x': 0.5, 'center_y': 0.7},
                text = labelText,
                halign = 'center',
                font_size = "20sp"
            )
            
            # Creates an "Okay" Button
            okayButton = Button(
                size_hint = (0.5, 0.1),
                pos_hint = {'center_x': 0.5, 'center_y': 0.3},
                text = "Okay"
            )
            
            # Binds the button to the self.closeCustomPopup function so that pressing the button will close the popup
            okayButton.bind(on_release = self.closeCustomPopup)
            
            # Adds the button and label widgets to the popup
            self.customPopup.content.add_widget(messageLabel)
            self.customPopup.content.add_widget(okayButton)
            
            # Opens the popup
            self.customPopup.open()
            
            return currentScreen
        
    # Called by pressing the Execute Task button
    # Checks if it's possible to execute the task (device is connected/the task is applicable)
    # Opens the appropriate popups
    def executeTask(self):
        if TaskManager.checkNone(): # None of actions are empty or have empty parameters
            
            # Whether the task given extends the syringe out of range (less than 0 or greater than 3000)
            # Equal to False if within bounds or a string representing the error message if out of bounds
            outOfBounds = TaskManager.checkOutOfBounds()
            if not outOfBounds == False: # The task causes the pump to go out of bounds and the appropriate error message is displayed
                self.makeCustomPopup(outOfBounds)
            elif SerialManager.makeConnection(): # Since the task is valid, an attempt is made at making a connection
                self.makeExecutionPopup() # Connection was successful, opening execution popup
                SerialManager.executeTask(TaskManager.newTaskActions) # Executing task using the task in newTaskActions
            else: # Connection was unsuccessful
                self.makeCustomPopup("No Connected\nDevice Found") 
        else: # At least on action is empty or has empty parameters
            self.makeCustomPopup("Some Actions Are\nIncomplete")
            
    # Generates a custom popup with the text given in the parameter
    def makeCustomPopup(self, textParameter):
        self.customPopup = Popup(title = "Warning",
                                 content = FloatLayout(size = self.size),
                                 size_hint = (0.5, 0.8))
        
        # Creates a label that will display the message in the textParameter to the user
        messageLabel = Label(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.7},
            text = textParameter,
            halign = 'center',
            font_size = "20sp"
        )
        
        # Creates an "Okay" button
        okayButton = Button(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.3},
            text = "Okay"
        )
        
        # Binds the Okay Button to self.closeCustomPopup which will close the popup
        okayButton.bind(on_release = self.closeCustomPopup)
        
        # Adds the label and button to the popup
        self.customPopup.content.add_widget(messageLabel)
        self.customPopup.content.add_widget(okayButton)
        
        # Opens popup
        self.customPopup.open()
        
    # Creates a popup that is opened when a task is executed
    def makeExecutionPopup(self):
        self.executionPopup = Popup(title = "Executing Task",
                                    content = FloatLayout(size = self.size),
                                    size_hint = (0.5, 0.8),
                                    auto_dismiss = False)
        
        # Message label, onto which the status of the task execution is displayed
        messageLabel = Label(size_hint = (0.5, 0.1),
                             id = "message_label",
                             pos_hint = {'center_x': 0.5, 'center_y': 0.7},
                             text = "Initializing...",
                             halign = 'center',
                             font_size = "20sp",            
        )
        
        # Binds the messageLabel to self.messageLabelCallback, so that the function is called every time the text changes
        # This allows that function to respond to changes in the task execution
        messageLabel.bind(text = self.messageLabelCallback)
        
        # Sets this messageLabel as a class variable in SerialManager so that the label is updated when the execution status changes
        SerialManager.setExecutionTextObject(messageLabel)
        
        # Creates a Stop Button that will halt the current execution of task
        stopButton = Button(id = "stop_button",
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.3},
            text = "Stop Task"
            )
        
        # Binds the stopButton to self.stopTaskButton so that task can be stopped when the button is pressed
        stopButton.bind(on_release = self.stopTaskButton)
        
        # Adds the label and the button to the popup
        self.executionPopup.content.add_widget(messageLabel)
        self.executionPopup.content.add_widget(stopButton)
        
        # Opens the popup
        self.executionPopup.open()
        
    # A callback function that is called whenever the message label in the execution popup changes text
    def messageLabelCallback(self, instance, text):
        if text == "Task Completed" or text == "Task Stopped": # Activates option to Close Window once the task is either completed or stopped
            for widget in instance.parent.children:
                if widget.id == "stop_button":
                    widget.bind(on_release = self.executionPopup.dismiss)
                    widget.text = "Close Window"
        
    # A callback function that is called whenever the stop task button is pressed in the execution popup
    def stopTaskButton(self, instance):
        SerialManager.stopTask()
        
    # Updates the text of the widget when given the index of the parameter in self.currentPopupValues, which is a list of the current values of the parameters of the action
    def updateWidgetText(self, widget, parameterIndex):
        widget.text = str(self.currentPopupValues[parameterIndex])
    
    # Creates an empty action and adds it to the task and screen
    # A new row is added to the Scrollable Layout accordingly
    def addEmptyAction(self):
        
        # A row in the Scrollable Layout, which represents the properties of a single task
        layout = FloatLayout(
            )
        
        # Creates a label to display the position of the task (1, 2, etc...)
        taskLabel = Label(
            id = "task_label",
            text = str(len(TaskManager.newTaskActions)+1),
            size_hint = (0.15, 1),
            pos_hint = {'center_x': 0.08, 'center_y': 0.5}
            )
        
        # Creates a spinner that allows the user to select a mode
        spinner = Spinner(text = "Choose Mode",
                          id = "mode_spinner",
                          values = ('Dispense', 'Retrieve', 'Back-and-Forth', 'Recycle'),
                          size_hint = (0.3, 1),
                          pos_hint = {'center_x': 0.3, 'center_y': 0.5}
                          )
        
        # Binds the spinner to self.updateModeSpinner so that each time a new mode is selected, the change is recorded
        spinner.bind(text = self.updateModeSpinner)
        
        # Adds a details button which both opens a popup on press
        # Allows the user to edit the details of the action (valve, volume, etc...)
        # After details are set, the popup will display a summary of the details
        detailsButton = Button(
            id = "details_button",
            text = "Choose a Mode First",
            size_hint = (0.5, 1),
            pos_hint = {'center_x': 0.725, 'center_y': 0.5},
            disabled = True
            )
        
        # Bind the button to self.editButtonCallback so that edit details popup is opened on pressing the button
        detailsButton.bind(on_release = self.editButtonCallback)
        
        # Adds the label, spinner, and button to the row
        layout.add_widget(taskLabel)
        layout.add_widget(spinner)
        layout.add_widget(detailsButton)
        
        # Adds the newly created row to the list of rows in TaskManager.taskRows, for easy reference later on
        TaskManager.taskRows.append(layout)
        
        # Adds the row to the main Scrollable Layout, which stores all of the actions/rows
        self.actions_layout.add_widget(layout)
        
        # Updates the running task dictionary in TaskManager with a new, empty element
        TaskManager.newTaskActions.update({str(len(TaskManager.newTaskActions)+1): [None, None]})
        
        return layout
        
    # A callback function that is called when the text value of a mode spinner changes
    # This updates the value of the Task Dictionary and the text of widgets on the screen
    def updateModeSpinner(self, spinner, value):
        # Sets the mode in the running dictionary at the index of the action to that of the spinner
        TaskManager.newTaskActions[str(TaskManager.taskRows.index(spinner.parent)+1)][0] = value
        
        # Sets the second entry in the actions list to None, which represents the parameters like volume, valve, time, speed
        TaskManager.newTaskActions[str(TaskManager.taskRows.index(spinner.parent)+1)][1] = None
        
        # Iterates through each widget of the row that the spinner is in to the find the details button
        # The text on the details button is set to "Add Details" to indicate that the details are empty and need to be set
        for widget in spinner.parent.children:
            if widget.id == "details_button":
                widget.disabled = False
                widget.text = "Add Details"
                return
            
    # A callback function that is called when the edit button is pressed
    # If "deletedToggled" is true, the action associated with the button is deleted
    # Otherwise, the detail editor is opened
    def editButtonCallback(self, button):
        if(self.deleteToggled):
            self.deleteAction(TaskManager.taskRows.index(button.parent)+1)
        else:
            self.openDetailEditor(button)
            
    # Called to initialize popup for detail editor
    # Initializes the values in self.currentPopupValues depending on the mode of the associated action
    # self.currentPopupValues keeps track of the values inputed by the user
    def openDetailEditor(self, button):
        mode = TaskManager.newTaskActions[str(TaskManager.taskRows.index(button.parent)+1)][0]
        index = str(TaskManager.taskRows.index(button.parent) + 1)
        
        # Initializes self.currentPopupValues, which stores the user inputs for the details of the popup (valve, volume, etc) when open
        # self.currentPopup is initialized as a list with the correct number of elements, matching the respective mode
        # Alternatively, if the running Task Dictionary already has values for details, those are used instead
        if mode == "Dispense" or mode == "Retrieve":
            self.currentPopupValues = self.getCurrentValues([None, None, None], index)
            self.popup = self.getDefaultPopup(index) # Opens a popup with a Valve Spinner, Volume Input, and Speed Input
        elif mode == "Back-and-Forth":
            self.currentPopupValues = self.getCurrentValues([None, None, None, None], index)
            self.popup = self.getTimePopup(index) # Opens a popup with a Valve Spinner, Volume Input, Speed Input, and Time Length Input
        elif mode == "Recycle":
            self.currentPopupValues = self.getCurrentValues([None, None, None, None, None], index)
            self.popup = self.getTimeAndExtraValvePopup(index) # Opens a popup with a Valve Spinner, Volume Input, Speed Input, Time Length Input and Extra Valve Input
            
    # Returns the text to be displayed on a widget given its index in a taskDictionary
    # Alternate values are the list to be returned if there are no details for that action (all elements are None)
    def getCurrentValues(self, alternateValues, index):
        if TaskManager.newTaskActions[str(index)][1] == None: # There are no details for that action
            return alternateValues # Return alternative list e.g. [None, None, None, None]
        else: # There are details for that action
            return TaskManager.newTaskActions[str(index)][1] # Returning the list of details/parameters at that index in the running task list
            
    # A callback function that is called when the valve spinner of the popup changes
    # Changes values in self.currentPopupValues based on what the value of the text of the widget is
    def valveSpinnerCallback(self, instance, value):
        try:
            self.currentPopupValues[0] = int(value)
        except:
            self.currentPopupValues[0] = None
        
    # A callback function that is called when volume textinput of the popup changes value
    # Changes values in self.currentPopupValues based on what the value of the text of the widget is
    def volumeTextInputCallback(self, instance, value):
        try:
            self.currentPopupValues[1] = int(value)
        except:
            self.currentPopupValues[1] = None
        
    # A callback function that is called when speed textinput of the popup changes value
    # Changes values in self.currentPopupValues based on what the value of the text of the widget is
    def speedTextInputCallback(self, instance, value):
        try:
            self.currentPopupValues[2] = int(value)
        except:
            self.currentPopupValues[2] = None
            
    # A callback function that is called when time textinput of the popup changes value
    # Changes values in self.currentPopupValues based on what the value of the text of the widget is
    def timeTextInputCallback(self, instance, value):
        try:
            self.currentPopupValues[3] = int(value)
        except:
            self.currentPopupValues[3] = None
            
    # A callback function that is called when the second valve spinner of the popup changes
    # Changes values in self.currentPopupValues based on what the value of the text of the widget is
    def secondValveSpinnerCallback(self, instance, value):
        try:
            self.currentPopupValues[4] = int(value)
        except:
            self.currentPopupValues[4] = None
    
    # A callback function that is called when the confirm button is pressed on the default popup
    # If the inputed values are invalid, a new popup is opened to warn the user about it.
    # Otherwise, the values are accepted into the TaskManager.newTaskActions dictionary
    def defaultPopupConfirmCallback(self, instance):
        
        # Gets the index of the popup (in terms of its step in the task) by splicing the title of its popup (grandparent widget)
        index = instance.parent.parent.parent.parent.title[13:]
        
        # Checks if the details/parameters entered by the user are valid
        if(TaskManager.checkParameters([TaskManager.newTaskActions[index][0], self.currentPopupValues])): # The inputs are valid
            TaskManager.newTaskActions[index][1] = self.currentPopupValues # The details/parameters in the main task dictionary are set to the ones inputed
            
            self.popup.dismiss() # Closes the popup and returns to the main Task Creator
            
            # Finds the details button matching the action
            for widget in TaskManager.taskRows[int(index)-1].children:
                if widget.id == "details_button":
                    widget.text = TaskManager.getDetails(TaskManager.newTaskActions[index]) # Changes the details text to a generated description
        else: # The user inputs are invalid
            # A popup is generated to notify the user that the input is invalid
            self.customPopup = Popup(title = "Warning",
                                     content = FloatLayout(size = self.size),
                                     size_hint = (0.5, 0.8))
            
            # Label which will display "Your Input Was Invalid"
            messageLabel = Label(
                size_hint = (0.5, 0.1),
                pos_hint = {'center_x': 0.5, 'center_y': 0.7},
                text = "Your Input Was\nInvalid",
                halign = 'center',
                font_size = "20sp"
            )
            
            # Okay Button which will close the popup
            okayButton = Button(
                size_hint = (0.5, 0.1),
                pos_hint = {'center_x': 0.5, 'center_y': 0.3},
                text = "Okay"
            )
            okayButton.bind(on_release = self.closeCustomPopup) # Binds the Okay Button to self.closeCustomPopup()
            
            # Adds the label and the button to the popup
            self.customPopup.content.add_widget(messageLabel)
            self.customPopup.content.add_widget(okayButton)
            
            self.customPopup.open() # Opens the popup
    
    # Callback button the cancels the Edit Popup
    def defaultPopupCancelCallback(self, instance):
        self.popup.dismiss()
    
    # Callback function that closes the notify popup
    def closeCustomPopup(self, instance):
        self.customPopup.dismiss()
    
    # Returns a newly generated popup
    # Contains the following widgets:
        #Valve Spinner
        #Volume Text Input
        #Speed Text Input
    def getDefaultPopup(self, index):
        
        # Checks if all of the values in self.currentPopupValues are empty
        # This is importing when opening a popup for an action which already has details/parameters set
        currentPopupValuesIsEmpty = True 
        for value in self.currentPopupValues:
            if value != None:
                currentPopupValuesIsEmpty = False
                break
        
        popup = Popup(title = "Editing Step " + index, # Sets the title of popup so it looks like this: "Editing Step 11"
                      content = FloatLayout(size = self.size),
                      size_hint = (0.5, 0.8))
        
        # Creates a valve spinner, which allows the user to select the valve of used during the action
        valve = Spinner(
            size_hint = (0.6, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.75},
            text = "Select Valve",
            values = ('1', '2', '3', '4', '5', '6') # The valves that the user can select are numbered 1-6
            )
        if not currentPopupValuesIsEmpty: # Updates the text on the spinner if values are already entered for that parameter
            self.updateWidgetText(valve, 0)
        valve.bind(text = self.valveSpinnerCallback) # self.valveSpinnerCallback is called on selection so that self.currentPopupValues is updated
        
        # Creates a label that displays a title above the Valve Spinner
        valveLabel = Label(
            pos_hint = {"center_x": 0.5, "center_y": 0.85},
            text = "Valve:",
            halign = "center"
            )
        
        # Creates a Text Input to input the volume of liquid to used for the action
        volumeInput = TextInput(
            size_hint = (0.6, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.6},
            hint_text = "Volume (1 - 3000 steps)",
            multiline = False,
            input_filter = 'int'
            )
        if not currentPopupValuesIsEmpty: # Updates the text in the text input if values are already entered for that parameter
            self.updateWidgetText(volumeInput, 1)
        volumeInput.bind(text = self.volumeTextInputCallback) # self.volumeTextCallback is called on selection so that self.currentPopupValues is updated
        
        # Creates a Text Input to input the speed that the syringe will be for the action
        speedInput = TextInput(
            size_hint = (0.6, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.45},
            hint_text = "Speed (1 Fastest, 40 Slowest)",
            multiline = False,
            input_filter = 'int'
            )
        if not currentPopupValuesIsEmpty: # Updates the text in the text input if values are already entered for that parameter
            self.updateWidgetText(speedInput, 2)
        speedInput.bind(text = self.speedTextInputCallback) # self.speedTextInputCallback is called on selection so that self.currentPopupValues is updated
        
        # Creates a confirm button
        # Button checks if the values that user selected for the parameters are correct
        # If the values are correct, self.currentPopupValues is inserted into the main Task Dictionary (self.newTaskActions)
        # In addition, the popup is closed and the Details Button displays a description of the values in a human-readable form
        confirmButton = Button(
            size_hint = (0.45, 0.1),
            pos_hint = {'center_x': 0.25, 'center_y': 0.3},
            text = "Confirm"
            )
        confirmButton.bind(on_release = self.defaultPopupConfirmCallback) # Calls self.defaultPopupConfirmCallback on press
        
        # Creates a cancel button which closes the popup
        cancelButton = Button(
            size_hint = (0.45, 0.1),
            pos_hint = {'center_x': 0.75, 'center_y': 0.3},
            text = "Cancel"
            )
        cancelButton.bind(on_release = self.defaultPopupCancelCallback) # Calls self.defaultPopupCancelCallback which closes the popup
        
        # Adds all of the widgets created in this function to the popup
        popup.content.add_widget(valveLabel)
        popup.content.add_widget(valve)
        popup.content.add_widget(volumeInput)
        popup.content.add_widget(speedInput)
        popup.content.add_widget(confirmButton)
        popup.content.add_widget(cancelButton)
        
        popup.open() # Opens the popup
        
        return popup # Returns the popup, so it can be saved to a variable if needed
    
    #Returns a newly generated popup with an added widget for time
    #Contains the following widgets:
        #Valve Spinner
        #Volume Text Input
        #Speed Text Input
        #Time Text Input
    def getTimePopup(self, index):
        
        # Checks if all of the values in self.currentPopupValues are empty
        # This is importing when opening a popup for an action which already has details/parameters set
        currentPopupValuesIsEmpty = True
        for value in self.currentPopupValues:
            if value != None:
                currentPopupValuesIsEmpty = False
        
        popup = Popup(title = "Editing Step " + index, # Sets the title of popup so it looks like this: "Editing Step 11"
                      content = FloatLayout(size = self.size),
                      size_hint = (0.5, 0.8))
        
        # Creates a valve spinner, which allows the user to select the valve of used during the action
        valve = Spinner(
            size_hint = (0.6, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.75},
            text = "Select Valve",
            values = ('1', '2', '3', '4', '5', '6') # The valves that the user can select are numbered 1-6
            )
        if not currentPopupValuesIsEmpty: # Updates the text in the spinner if values are already entered for that parameter
            self.updateWidgetText(valve, 0)
        valve.bind(text = self.valveSpinnerCallback) # self.valveSpinnerCallback is called on selection so that self.currentPopupValues is updated
        
        # Creates a label that displays a title above the Valve Spinner
        valveLabel = Label(
            pos_hint = {"center_x": 0.5, "center_y": 0.85},
            text = "Valve:",
            halign = "center"
            )
        
        # Creates a Text Input to input the volume of liquid to used for the action
        volumeInput = TextInput(
            size_hint = (0.6, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.6},
            hint_text = "Volume (1 - 3000 steps)",
            multiline = False,
            input_filter = 'int'
            )
        if not currentPopupValuesIsEmpty: # Updates the text in the text input if values are already entered for that parameter
            self.updateWidgetText(volumeInput, 1)
        volumeInput.bind(text = self.volumeTextInputCallback) # self.volumeTextCallback is called on selection so that self.currentPopupValues is updated
        
        # Creates a Text Input to input the speed that the syringe will be for the action
        speedInput = TextInput(
            size_hint = (0.6, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.45},
            hint_text = "Speed (1 Fastest, 40 Slowest)",
            multiline = False,
            input_filter = 'int'
            )
        if not currentPopupValuesIsEmpty: # Updates the text in the text input if values are already entered for that parameter
            self.updateWidgetText(speedInput, 2)
        speedInput.bind(text = self.speedTextInputCallback) # self.speedTextInputCallback is called on selection so that self.currentPopupValues is updated
        
        # Creates a Time Input to input the length of time that the action should run
        timeInput = TextInput(
            size_hint = (0.6, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.3},
            hint_text = "Time (Seconds)",
            multiline = False,
            input_filter = 'int'
            )
        if not currentPopupValuesIsEmpty: # Updates the text in the text input if values are already entered for that parameter
            self.updateWidgetText(timeInput, 3)
        timeInput.bind(text = self.timeTextInputCallback) # self.timeTextInputCallback is called on selection so that self.currentPopupValues is updated

        # Creates a confirm button
        # Button checks if the values that user selected for the parameters are correct
        # If the values are correct, self.currentPopupValues is inserted into the main Task Dictionary (self.newTaskActions)
        # In addition, the popup is closed and the Details Button displays a description of the values in a human-readable form
        confirmButton = Button(
            size_hint = (0.45, 0.1),
            pos_hint = {'center_x': 0.25, 'center_y': 0.15},
            text = "Confirm"
            )
        confirmButton.bind(on_release = self.defaultPopupConfirmCallback) # Calls self.defaultPopupConfirmCallback on press
        
        # Creates a cancel button which closes the popup
        cancelButton = Button(
            size_hint = (0.45, 0.1),
            pos_hint = {'center_x': 0.75, 'center_y': 0.15},
            text = "Cancel"
            )
        cancelButton.bind(on_release = self.defaultPopupCancelCallback) # Calls self.defaultPopupCancelCallback which closes the popup
        
        # Adds all of the widgets created in this function to the popup
        popup.content.add_widget(valveLabel)
        popup.content.add_widget(valve)
        popup.content.add_widget(volumeInput)
        popup.content.add_widget(speedInput)
        popup.content.add_widget(timeInput)
        popup.content.add_widget(confirmButton)
        popup.content.add_widget(cancelButton)
        
        popup.open() # Opens the popup
        
        return popup # Returns the popup, so it can be saved to a variable if needed
    
    #Returns a newly generated popup with an added widget for time
    #Contains the following widgets:
        #Main Valve Spinner
        #Bypass Valve Spinner
        #Volume Text Input
        #Speed Text Input
        #Time Text Input
    def getTimeAndExtraValvePopup(self, index):
        
        # Checks if all of the values in self.currentPopupValues are empty
        # This is importing when opening a popup for an action which already has details/parameters set
        currentPopupValuesIsEmpty = True
        for value in self.currentPopupValues:
            if value != None:
                currentPopupValuesIsEmpty = False
        
        popup = Popup(title = "Editing Step " + index, # Sets the title of popup so it looks like this: "Editing Step 11"
                      content = FloatLayout(size = self.size),
                      size_hint = (0.5, 0.8))
        
        # Creates a valve spinner, which allows the user to select the input valve used during the action
        valve = Spinner(
            size_hint = (0.45, 0.1),
            pos_hint = {'center_x': 0.25, 'center_y': 0.75},
            text = "Select Valve",
            values = ('1', '2', '3', '4', '5', '6')
            )
        if not currentPopupValuesIsEmpty: # Updates the text in the spinner if values are already entered for that parameter
            self.updateWidgetText(valve, 0)
        valve.bind(text = self.valveSpinnerCallback) # self.valveSpinnerCallback is called on selection so that self.currentPopupValues is updated
        
        # Creates a valve spinner, which allow the user to select the output valve used during the action
        extraValve = Spinner(
            size_hint = (0.45, 0.1),
            pos_hint = {'center_x': 0.75, 'center_y': 0.75},
            text = "Select Valve",
            values = ('1', '2', '3', '4', '5', '6')
            )
        if not currentPopupValuesIsEmpty: # Updates the text in the spinner if values are already entered for that parameter
            self.updateWidgetText(extraValve, 4)
        extraValve.bind(text = self.secondValveSpinnerCallback) # self.valveSpinnerCallback is called on selection so that self.currentPopupValues is updated
        
        # Creates a label that displays a title above the Output Valve Spinner
        valveLabel = Label(
            pos_hint = {"center_x": 0.25, "center_y": 0.85},
            text = "Output Valve:",
            halign = "center"
            )
        
        # Creates a label that displays a title above the Input Valve Spinner
        extraValveLabel = Label(
            pos_hint = {"center_x": 0.75, "center_y": 0.85},
            text = "Input Valve:",
            halign = "center"
            )
        
        # Creates a Text Input to input the volume of liquid to used for the action
        volumeInput = TextInput(
            size_hint = (0.6, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.6},
            hint_text = "Volume (1 - 3000 steps)",
            multiline = False,
            input_filter = 'int'
            )
        if not currentPopupValuesIsEmpty: # Updates the text in the text input if values are already entered for that parameter
            self.updateWidgetText(volumeInput, 1)
        volumeInput.bind(text = self.volumeTextInputCallback) # self.volumeTextCallback is called on selection so that self.currentPopupValues is updated
        
        # Creates a Text Input to input the speed that the syringe will be for the action
        speedInput = TextInput(
            size_hint = (0.6, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.45},
            hint_text = "Speed (1 Fastest, 40 Slowest)",
            multiline = False,
            input_filter = 'int'
            )
        if not currentPopupValuesIsEmpty: # Updates the text in the text input if values are already entered for that parameter
            self.updateWidgetText(speedInput, 2)
        speedInput.bind(text = self.speedTextInputCallback) # self.speedTextInputCallback is called on selection so that self.currentPopupValues is updated
        
        # Creates a Time Input to input the length of time that the action should run
        timeInput = TextInput(
            size_hint = (0.6, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.3},
            hint_text = "Time (Seconds)",
            multiline = False,
            input_filter = 'int'
            )
        if not currentPopupValuesIsEmpty: # Updates the text in the text input if values are already entered for that parameter
            self.updateWidgetText(timeInput, 3)
        timeInput.bind(text = self.timeTextInputCallback) # self.timeTextInputCallback is called on selection so that self.currentPopupValues is updated
        
        # Creates a confirm button
        # Button checks if the values that user selected for the parameters are correct
        # If the values are correct, self.currentPopupValues is inserted into the main Task Dictionary (self.newTaskActions)
        # In addition, the popup is closed and the Details Button displays a description of the values in a human-readable formsssssssss
        confirmButton = Button(
            size_hint = (0.45, 0.1),
            pos_hint = {'center_x': 0.25, 'center_y': 0.15},
            text = "Confirm"
            )
        confirmButton.bind(on_release = self.defaultPopupConfirmCallback) # Calls self.defaultPopupConfirmCallback on press
        
        # Creates a cancel button which closes the popup
        cancelButton = Button(
            size_hint = (0.45, 0.1),
            pos_hint = {'center_x': 0.75, 'center_y': 0.15},
            text = "Cancel"
            )
        cancelButton.bind(on_release = self.defaultPopupCancelCallback) # Calls self.defaultPopupCancelCallback which closes the popups
        
        # Adds all of the widgets created in this function to the popup
        popup.content.add_widget(valveLabel)
        popup.content.add_widget(extraValveLabel)
        popup.content.add_widget(valve)
        popup.content.add_widget(extraValve)
        popup.content.add_widget(volumeInput)
        popup.content.add_widget(speedInput)
        popup.content.add_widget(timeInput)
        popup.content.add_widget(confirmButton)
        popup.content.add_widget(cancelButton)
        
        popup.open() # Opens the popup
        
        return popup # Returns the popup, so it can be saved to a variable if needed
     
     
#Acts as a container for the Debug Screen
class DebugScreen(Screen):

    # Called by pressing the Execute Task button
    # Checks if the device is connected
    # Opens the appropriate popups
    def executeRawCommands(self):
        if self.rawCommandText.text != "":
            
            if SerialManager.makeConnection():
                response = SerialManager.executeRawCommand(self.rawCommandText.text)
                self.rawCommandConsole.text = response
            else:
                self.makeCustomPopup("No Connected\nDevice Found")
        else:
            self.makeCustomPopup("Input is Empty")
            
    # Generates a notification popup with the text given in the parameter
    def makeCustomPopup(self, textParameter):
        self.popup = Popup(title = "Warning",
                                 content = FloatLayout(size = self.size),
                                 size_hint = (0.5, 0.8))
        
        okayLabel = Label(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.7},
            text = textParameter,
            halign = 'center',
            font_size = "20sp"
        )
        
        okayButton = Button(
            size_hint = (0.5, 0.1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.3},
            text = "Okay"
        )
        okayButton.bind(on_release = self.closePopup)
        
        self.popup.content.add_widget(okayLabel)
        self.popup.content.add_widget(okayButton)
        
        self.popup.open()
     
     # Closes the current open popup
    def closePopup(self, instance):
        self.popup.dismiss()
     
#Allows the reader to load a previously saved file and use that
class PreviousFileScreen(Screen):
    def getPath(self):
        return  FileManager.shortenFilePath(os.path.dirname(os.path.realpath(__file__)))+ "/Tasks"
    #recieves the file path from the file chooser
    def selectFile(self, *args):
        try:
            FileManager.setPath(args[1][0])
        except:
            pass
        
    # Refreshes the filechooser so that new files are displayed
    def refresh(self):
        self.filechooser._update_files()
    
    #signals the widgets to update based on the selected file
    def updateDisplay(self, object):
        current_dict = FileManager.importFile()
        if current_dict!= None:
            object.replaceTask(current_dict)


# Loads the .kv file needed
kv = Builder.load_file("Interface.kv")


# Builds the app
class MainApp(App):

    def build(self):
        return kv


# Main Function which runs the app
if __name__ == "__main__":
    MainApp().run()