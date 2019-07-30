import threading
import time

class ThreadUpdater(threading.Thread):
    def __init__(self, mode, interval):
        threading.Thread.__init__(self)

        self.mode = mode
        self.interval = interval

        self.event = threading.Event()

    def run(self):
        while not self.event.is_set():
            self.mode()
            self.event.wait(self.interval)

    def stop(self):
        self.event.set()

""" Example Code for Using ThreadUpdater

def queryUpdate():
    print("yo")

queryTimer = ThreadUpdater(queryUpdate, 1)
queryTimer.start()

time.sleep(10)

queryTimer.stop()

print("done")

"""