import serial
import time
from ThreadManager import ThreadUpdater

class SerialManager(object):
    def __init__(self):
        self.ser = None #serial.Serial('/dev/ttyS0', baudrate = 9600,
                    #parity = serial.PARITY_NONE,
                    #stopbits = serial.STOPBITS_ONE,
                    #bytesize = serial.EIGHTBITS)
        
    def sendCommand(self, command):
        ser.write((command+"\r").encode())
        
    def queryUpdate(self):
        #Write Goes Here
        #Read Goes Here
        print(time.localtime())
        
    def startQueryUpdate(self):
        self.queryUpdater = ThreadUpdater(self.queryUpdate, 1)
        self.queryUpdater.start()
        
    def stopQueryUpdate(self):
        self.queryUpdater.stop()
        
serial_object = SerialManager()