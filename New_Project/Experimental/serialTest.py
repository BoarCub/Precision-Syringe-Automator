import serial
import serial.tools.list_ports
import time

class Pump:
    
    def __init__(self):
        
        self.VID = 1659
        self.PID = 8963
        
        self.ser = serial.Serial(self.getPortOfDevice(self.VID, self.PID), 9600, timeout =5)
        self.shouldRepeat = True
        self.response = ""
        
    def sendMessage(self):
        #self.ser.write('/1YI1A3000O6A2900R\r'.encode())
        self.ser.write('/1I1A3000O6A0G3R\r'.encode())
        #self.ser.write('/1TR\r'.encode())
        self.response = self.ser.read().decode()      
        print("response: ", self.response)
        
    def backAndForth(self):
        
        constant = 100
        
        #self.ser.write('/1ZI4A3000O6A0R\r'.encode())
        #self.ser.write('/1YI1A3000O6R\r'.encode())
        self.ser.write('/1A2675A3000G10A3000I1A0O6A500I1A0R\r'.encode())
        #self.ser.write('/1A3000I1A0O6A500I1A0R\r'.encode())
        print(self.ser.readline().decode())
        self.ser.write('/1Q\r'.encode())
        print(self.ser.readline().decode())
        
    def repeatPump(self):
        self.ser.write('/1YS10R\r'.encode())
        self.ser.readline()
        
        for i in range(2):
            self.ser.write('/1Q\r'.encode())
            query = self.ser.readline()
            try:
                query = query.decode()[2]
            except:
                query = '@'
            while query == '@':
                time.sleep(0.5)
                self.ser.write('/1Q\r'.encode())
                query = self.ser.readline().decode()[2]
                
            self.ser.write('/1I1A3000O6A0R\r'.encode())
            self.ser.readline()
            
        time.sleep(1)
        print("Wassup!")
        self.interruptCycle()
            
    def backAndForthUpdated(self):
        self.ser.write('/1YS20I1A3000O6R\r'.encode())
        self.ser.readline()
        
        for i in range(10):
            self.ser.write('/1Q\r'.encode())
            query = self.ser.readline()
            try:
                query = query.decode()[2]
            except:
                query = '@'
            while query == '@':
                time.sleep(0.5)
                self.ser.write('/1Q\r'.encode())
                query = self.ser.readline().decode()[2]
                
            self.ser.write('/1A2675A3000R\r'.encode())
            self.ser.readline()
            
        self.ser.write('/1Q\r'.encode())
        query = self.ser.readline()
        try:
            query = query.decode()[2]
        except:
            query = '@'
        while query == '@':
            time.sleep(0.5)
            self.ser.write('/1Q\r'.encode())
            query = self.ser.readline().decode()[2]
        self.ser.write('/1A3000I1A0O6A1000I1A0R\r'.encode())
        self.ser.readline()
            
    def interruptCycle(self):
        self.ser.write('/1T\r'.encode())
        self.ser.readline()
        self.ser.write('/1?\r'.encode())
        print(self.ser.readline().decode())
        
    def getPortOfDevice(self, vid, pid):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.vid == vid and port.pid == pid:
                return port.device
        raise EnvironmentError('No supported devices available')
    
    def getPositionTest(self):
        self.ser.write('/1?\r'.encode())
        rawPosition = self.ser.readline().decode()[3:-3]
        print(rawPosition)
        
obj = Pump()
obj.getPositionTest()
obj.backAndForthUpdated()