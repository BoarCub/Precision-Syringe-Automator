from ThreadManager import *
import time

class tester():
    def __init__(self):
        self.datetime = time.time()
        self.initialTime = self.datetime
        self.ThreadManager = ThreadUpdater(self.update, 1)
        self.ThreadManager.run()
        
    def update(self):
        print(time.time())
        if (time.time() > self.initialTime + 10):
            self.ThreadManager.stop()
            
tester = tester()
        
        