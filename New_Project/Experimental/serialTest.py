import serial

class Pump:
    
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout =5)
        self.shouldRepeat = True
        self.response = ""
        
    def sendMessage(self):
        self.ser.write('/1A3000R\r'.encode())
        
obj = Pump()
obj.sendMessage()