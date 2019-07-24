from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.dropdown import DropDown

class MainWindow(Screen):
    pass

class NewRoutineWindow(Screen):
    pass

class NewTaskWindow(Screen):
    pass

class FileChooserWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("my.kv")

class MyMainApp(App):
    def build(self):
        return kv
    
if __name__ == "__main__":
    MyMainApp().run()