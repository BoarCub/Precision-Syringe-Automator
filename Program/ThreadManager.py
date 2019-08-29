import threading

"""
ThreadUpdater can loops a given function at the given time interval
Usage of ThreadUpdate looks like this:

def exampleFunction():
    whateverYouWant()
    print("lorem ipsum")
    
updater = ThreadUpdater(exampleFunction, 0.1) #This ThreadUpdater will run exampleFunction() every 0.1 seconds
updater.start() #Starts running updater (updater doesn't run at all before this)

~Some Code Here~

updater.stop() #Stops updater from executing exampleFunction

"""

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