import os

from DataManager import FileImporter
from SerialManager import *
from TaskCreator import *
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from serialManager import *

#each class is a window that is being called via the kv file

class MainWindow(Screen):
    pass

class NewRoutineWindow(Screen):
    pass

class NewTaskWindow(Screen):
        
    def addEmptyTask(self):
        taskcreator_object.actions.append([str(len(taskcreator_object.actions) + 1), 'Empty', 'Empty'])
        buttonTemp = Button(text=self.getButtonString(taskcreator_object.actions[len(taskcreator_object.action)-1]))
            
        buttonTemp.bind(on_release = self.callback)
        
        self.ids.grid.add_widget(buttonTemp)
        
        taskcreator_object.buttons.append(buttonTemp)
            
    def getButtonString(self, ls):
        str = 'Task '
        str += ls[0]
        str += '\nAction: '
        str += ls[1]
        str += '\nValue: '
        if ls[2] != '':
            str += ls[2]
        else:
            str += 'N/A'
        return str
    
    def callback(self, instance):
        self.editTask(instance.text)
    
    def getObjectFromID(self, parent, id):
        for child in parent.children:
            if child.id == id:
                return child
    
    def save(self, instance):
        
        self.getObjectFromID(self.editPopup.content, 'message_label').text = 'Saved...'
        
        try:
            valueParameter = int(self.getObjectFromID(self.editPopup.content, 'value_input').text)
        except:
            valueParameter = None
        
        if(self.spinnerText == None):
            self.getObjectFromID(self.editPopup.content, 'message_label').text = 'Select an Action'
        elif(FileImporter.checkValue(
            [
            FileImporter.all_commands[self.spinnerText],
            valueParameter
            ]
            )):
            
            index = int(self.editPopup.title[13:]) - 1
            
            taskcreator_object.actions[index][1] = self.spinnerText
            taskcreator_object.actions[index][2] = self.getObjectFromID(self.editPopup.content, 'value_input').text
            
            taskcreator_object.buttons[index].text = self.getButtonString(taskcreator_object.actions[index])
            
            self.editPopup.dismiss()
        else:
            self.getObjectFromID(self.editPopup.content, 'message_label').text = 'Inputed Value Does Not Match Action'
            
    def saveSpinnerText(self, spinner, text):
        self.spinnerText = text
        
        if( len((FileImporter.getValues()[FileImporter.all_commands[self.spinnerText]])) > 0):
            self.getObjectFromID(self.editPopup.content, 'value_input').disabled = False
        else:
            self.getObjectFromID(self.editPopup.content, 'value_input').disabled = True
        
        self.getObjectFromID(self.editPopup.content, 'value_input').text = ""
        self.getObjectFromID(self.editPopup.content, 'value_input').hint_text = self.returnHintText(text)

    def returnHintText(self, spinner_text):
        if (spinner_text == None):
            return "Enter Value"
        else:
            if ((FileImporter.getValues()[FileImporter.all_commands[self.spinnerText]])==[]):
                return "No Value Needed"
            else: return 'Type Value from '+ str(FileImporter.getValues()[FileImporter.all_commands[self.spinnerText]][0]) + ' to ' + str(FileImporter.getValues()[FileImporter.all_commands[self.spinnerText]][1])
    def editTask(self, buttonText):
        
        self.spinnerText = None
        
        lines = buttonText.splitlines()
        
        self.editPopup = Popup(title = "Editing " + lines[0],
                          content = BoxLayout(orientation='vertical', spacing = 50, size_hint=(0.6, 1), pos_hint = {'top': 1}),
                          size_hint = (None, None), size = (400, 400),
                          )
        
        spinner = Spinner(
            text = 'Select Action',
            values = FileImporter.all_commands,
            id = 'action_spinner',
            on_value = self.saveSpinnerText
            )
        
        spinner.bind(text = self.saveSpinnerText)
        
        valueInput = TextInput(
            id = 'value_input',
            hint_text = 'Choose an Action Before Typing Values',
            multiline = False,
            input_filter = 'int',
            disabled = True
            )
        
        saveButton = Button(
            id = 'save_button',
            text = 'Save',
            on_release = self.save
            )
        
        messageLabel = Label(
            id = 'message_label',
            text = 'Console'
            )
        
        self.editPopup.content.add_widget(spinner)
        self.editPopup.content.add_widget(valueInput)
        self.editPopup.content.add_widget(saveButton)
        self.editPopup.content.add_widget(messageLabel)
        self.editPopup.open()
                          
        pass
class LineByLineWindow(Screen):
    def getCommands(self):
        return FileImporter.all_commands

class ExecuteFileWindow(Screen):

    def startLoop(self):
        #serial_object.startQueryUpdate(self.ids.queryLabel)

        pass
    def stopLoop(self):
        #serial_object.stopQueryUpdate()
        pass

class SaveFileWindow(Screen):
    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write("hi")

    def getPath(self):
        return os.path.dirname(os.path.realpath(__file__)) + "/Routines" #sets default folder to FileChooser interface
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
