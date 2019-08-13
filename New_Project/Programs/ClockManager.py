from kivy.clock import Clock

import time

class Time():
    def updateTime(self, *args):
            print(time.asctime())
            
t = Time()
Clock.schedule_interval(t.updateTime, 1)

