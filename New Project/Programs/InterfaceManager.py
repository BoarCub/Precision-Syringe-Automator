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
        
        
# Path of .kv to import the user interface from 
KIVY_FILE = Builder.load_file("Interface.kv")
        

class MainApp(App):
    
    def build(self):
        return KIVY_FILE
    

# Main function which runs the app
if __name__ == "__main__":
    MainApp().run()
    

# InterfaceManager acts as a container for all of the Screens in the app
class InterfaceManager(ScreenManager):
    pass


# Container for StartMenu Screen
class StartScreen(Screen):
    pass