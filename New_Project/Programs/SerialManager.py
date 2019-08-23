from FileManager import *
from ThreadManager import *
from time import sleep
from time import time
import serial
import serial.tools.list_ports

class SerialManager(object):
    def __init__(self):
        
        #The below VID (Vendor ID) and PID (Product ID) constants are set by the manufacturer and are used to identify the USB Device
        #These values are imported from a json file
        distribution_database = FileManager.importFilePath(
            FileManager.shortenFilePath(os.path.dirname(os.path.realpath(__file__)))+ "/Databases/DistributionDatabase")
        self.VID = distribution_database["VID"]
        self.PID = distribution_database["PID"]
        
        #A boolean used to track whether a time-based task is active
        self.actionActive = False
        
        #Initial time used for time-based actions to know when the action started
        self.initialTime = None
        
        #Used in time-based actions, represents the number of seconds that should pass before the action stops
        self.actionLength = None
        
        #The index of the action currently being executed in the task
        self.actionIndex = None
        
        #The text object displayed in the user interface to give information about the task execution
        self.executionTextObject = None
    
    # Creates a new serial connection and returns a boolean indicating whether the connection was successfully made
    def makeConnection(self):
    
        try:
            self.ser.close()
        except:
            pass
        
        try:
            self.ser = serial.Serial(self.getPortOfDevice(self.VID, self.PID), 9600, timeout = 0.1)
        except:
            return False
        
        try:
            self.ser.write('/1Q\r'.encode())
            response = self.ser.readline().decode()
        except:
            return False
        
        if response == "":
            return False
        else:
            return True
        
    def setExecutionTextObject(self, obj):
        self.executionTextObject = obj
    
    #Returns the port/device name of the USB Device with the VID and PID given as the parameters
    def getPortOfDevice(self, vid, pid):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.vid == vid and port.pid == pid:
                return port.device
        raise EnvironmentError('No supported USB device available') 
    
    def executeTask(self, taskDictionary):
        
        self.makeConnection()
        
        self.task = taskDictionary
        self.actionIndex = 0
        
        self.runInitialization()
        self.executionTextObject.text = "Initializing..."
        
        self.looper = ThreadUpdater(self.taskLoop, 1)
        self.looper.start()
        
    def taskLoop(self):
        if not self.actionActive:
            if self.actionIndex == len(self.task):
                self.looper.stop()
                self.taskCompleted()
            else:
                self.actionIndex += 1
                actionInfo = self.task[str(self.actionIndex)]
                self.executionTextObject.text = "Executing Step " + str(self.actionIndex) + ":\n" + actionInfo[0]
                if actionInfo[0] == "Retrieve":
                    self.runRetrieve(actionInfo[1][0], actionInfo[1][1], actionInfo[1][2])
                elif actionInfo[0] == "Dispense":
                    self.runDispense(actionInfo[1][0], actionInfo[1][1], actionInfo[1][2])
                elif actionInfo[0] == "Back-and-Forth":
                    self.runBackAndForth(actionInfo[1][0], actionInfo[1][1], actionInfo[1][2], actionInfo[1][3])
                else:
                    self.runBypass(actionInfo[1][0], actionInfo[1][1], actionInfo[1][2], actionInfo[1][3], actionInfo[1][4])
                
    def taskCompleted(self):
        self.executionTextObject.text = "Task Completed"
        
    def stopTask(self):
        self.looper.stop()
        try:
            self.updater.stop()
        except:
            pass
        try:
            self.ser.write("/1T\r".encode())
        except:
            pass
        self.executionTextObject.text = "Task Stopped"
    
    # Runs Initialization on the Pump 
    def runInitialization(self):
        self.ser.write('/1YR\r'.encode())
        self.ser.readline()
        
        self.actionActive = True
        self.updater = ThreadUpdater(self.basicActionUpdate, 0.1)
        self.updater.start()
        
    # Runs the Retrieve Command on the Pump
    def runRetrieve(self, valve, volume, speed):
        command = '/1S' + str(speed) + 'I' + str(valve) + 'P' + str(volume) + 'R\r'
        self.ser.write(command.encode())
        self.ser.readline()
        
        self.actionActive = True
        self.updater = ThreadUpdater(self.basicActionUpdate, 0.1)
        self.updater.start()
        
    # Runs the Dispense Command on the Pump
    def runDispense(self, valve, volume, speed):
        command = '/1S' + str(speed) + 'O' + str(valve) + 'D' + str(volume) + 'R\r'
        self.ser.write(command.encode())
        self.ser.readline()
        
        self.actionActive = True
        self.updater = ThreadUpdater(self.basicActionUpdate, 0.1)
        self.updater.start()
        
    # An Update Function Called to Check if a One-Step Action is Completed
    def basicActionUpdate(self):
        try:
            self.ser.write('/1Q\r'.encode())
            query = self.ser.readline()
        except:
            self.stopTask()
            self.executionTextObject.text = "Could Not Connect\nTo Device"
        try:
            query = query.decode()
        except:
            query = '  @'
        
        if query == "":
            self.stopTask()
            self.executionTextObject.text = "Could Not Connect\nTo Device"
        elif query[2] != '@':
            self.updater.stop()
            self.actionActive = False
    
    # Runs the Back and Forth Action on the Pump
    def runBackAndForth(self, valve, volume, speed, length):
        self.initialTime = time()
        self.actionLength = length
        self.actionParameters = [valve, volume, speed]
        self.actionActive = True
        
        self.updater = ThreadUpdater(self.backAndForthUpdate, 0.1)
        self.updater.start()
        
    # Update Function that is Called to run the action again when completed, until the full length of time passes
    def backAndForthUpdate(self):
        if(time() > self.initialTime + self.actionLength):
            self.updater.stop()
            self.updater = ThreadUpdater(self.basicActionUpdate, 0.1)
            self.updater.start()
        else:
            try:
                self.ser.write('/1Q\r'.encode())
                query = self.ser.readline()
            except:
                self.stopTask()
                self.executionTextObject.text = "Could Not Connect\nTo Device"
            try:
                query = query.decode()
            except:
                query = '  @'
            if query == "":
                self.stopTask()
                self.executionTextObject.text = "Could Not Connect\nTo Device"
            elif query[2] != '@':        
                valve  = self.actionParameters[0]
                volume = self.actionParameters[1]
                speed = self.actionParameters[2]
                
                command = '/1S' + str(speed) + 'O' + str(valve) + 'D' + str(volume) + 'P' + str(volume) + 'R\r'
                self.ser.write(command.encode())
                self.ser.readline()
    
    # Runs the Bypass/Recycle Action on the Pump
    def runBypass(self, valve, volume, speed, length, bypassValve):
        self.initialTime = time()
        self.actionLength = length
        self.actionParameters = [valve, volume, speed, bypassValve]
        self.actionActive = True
        
        self.updater = ThreadUpdater(self.bypassUpdate, 0.1)
        self.updater.start()
        
    # Update Function that is Called to Run the Action Again When Completed, Until the Full Length of Time Passes
    def bypassUpdate(self):
        if(time() > self.initialTime + self.actionLength):
            self.updater.stop()
            self.updater = ThreadUpdater(self.basicActionUpdate, 0.1)
            self.updater.start()
        else:
            try:
                self.ser.write('/1Q\r'.encode())
                query = self.ser.readline()
            except:
                self.stopTask()
                self.executionTextObject.text = "Could Not Connect\nTo Device"
            try:
                query = query.decode()
            except:
                query = '  @'
            if query == "":
                self.stopTask()
                self.executionTextObject.text = "Could Not Connect\nTo Device"
            elif query[2] != '@':
                valve = self.actionParameters[0]
                volume = self.actionParameters[1]
                speed = self.actionParameters[2]
                bypassValve = self.actionParameters[3]
        
                command = '/1S' + str(speed) + 'O' + str(valve) + 'D' + str(volume) + 'I' + str(bypassValve) + 'P' + str(volume) + 'R\r'
                self.ser.write(command.encode())
                self.ser.readline()

    
SerialManager = SerialManager()