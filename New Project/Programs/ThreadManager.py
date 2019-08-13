import threading
import time

#ThreadUpdater object runs loops a given function based on parameters
class ThreadUpdater(threading.Thread):
    
    #function paramater is the function to be run and interval is the interval in seconds that the function will be looped
    def __init__(self, function, interval):
        threading.Thread.__init__(self) #inherits threading.Thread

        self.function = function
        self.interval = interval

        self.event = threading.Event()

    #starts running the loop
    def run(self):
        while not self.event.is_set():
            self.function()
            self.event.wait(self.interval)

    #ends the loop
    def stop(self):
        self.event.set()
        
datetime = time.time()
initialTime = 0

def update():
    if datetime > initialTime + 10:
        updater.stop()
        
updater = ThreadUpdater(update, 1)
intialTime = datetime

updater.run()