from kivy.clock import Clock

import time

class Time():
    
    def __init__(self):
        pass
    
    def updateTime(self, *args):
        print("yo")
        print(time.asctime())
            
    def start(self):
        Clock.schedule_interval(self.updateTime, 1)
    
t = Time()
t.start()

