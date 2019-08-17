import serial
from time import sleep
class Pump:
    
    def __init__(self):
        self.ser = serial.Serial('COM9', 9600, timeout =5)
        self.shouldRepeat = True
        self.response = ""
        
    def sendMessage(self):
        self.ser.write('/1Q\r'.encode())
        sleep(0)
        
        while True:
            self.response = self.ser.readline().decode()      
            print("response: ", self.response)
            if self.response != "":
                break
        
obj = Pump()
obj.sendMessage()