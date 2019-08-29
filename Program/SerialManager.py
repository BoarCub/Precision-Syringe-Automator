from FileManager import *
from ThreadManager import *
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
        
        #A boolean used to track whether an action is currently active
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
    
        # Closes the serial connection if currently open
        try:
            self.ser.close()
        except:
            pass
        
        # Attempts to open a new serial connection
        try:
            self.ser = serial.Serial(self.getPortOfDevice(self.VID, self.PID), 9600, timeout = 0.1)
        except:
            return False
        
        # Send a query through the serial connection to see if a pump responds
        try:
            self.ser.write('/1Q\r'.encode())
            response = self.ser.readline().decode()
        except:
            return False
        
        # Checks if the pump has a valid response
        if response == "":
            return False
        else:
            return True
        
    # Sets a class variable with label object to which the status of the task execution is displayed
    def setExecutionTextObject(self, obj):
        self.executionTextObject = obj
    
    # Returns the port/device name of the USB Device with the VID and PID given as the parameters
    def getPortOfDevice(self, vid, pid):
        ports = serial.tools.list_ports.comports() #Gets a list of all serial ports
        for port in ports:
            if port.vid == vid and port.pid == pid: #Checks that the VID and PID match with the settings
                return port.device #Returns the full address of the pump e.g. /dev/ttyUSB0
        raise EnvironmentError('No supported USB device available')
    
    # Executes a raw command given as a string e.g. A1000R
    # Returns a string representing the response (or lack of it) to be displayed
    def executeRawCommand(self, command):
        self.ser.write(("/1" + command + "\r").encode())
        try:
            return "Response: " + self.ser.readline().decode()
        except:
            return "No Response"
    
    # Executes a task when given a dictionary as the parameter
    # The dictionary is in the same format as the newTaskActions dictionary in TaskManager
    def executeTask(self, taskDictionary):
        
        # Gets correct actions ready
        self.task = taskDictionary
        self.actionIndex = 0
        
        # Runs initialization
        self.runInitialization()
        try:
            self.executionTextObject.text = "Initializing..."
        except:
            pass
        
        # Starts the taskLoop, which will update every second
        self.looper = ThreadUpdater(self.taskLoop, 1)
        self.looper.start()
        
    # A function that is called every second to continue to the next action in the task if the current action in the task is finished
    # The loop stops once the task runs out of actions or the task execution is interrupted
    def taskLoop(self):
        if not self.actionActive: #Executes once the current action is finished
            if self.actionIndex == len(self.task): #End of the task reached, ending task execution
                self.looper.stop()
                self.taskCompleted()
            else: #Still more actions let to execute
                self.actionIndex += 1 #Increasing index by one
                actionInfo = self.task[str(self.actionIndex)] #Getting a info of the task like mode, volume and speed
                
                # Sets the display text in the user interface with information of the step being executed
                try:
                    self.executionTextObject.text = "Executing Step " + str(self.actionIndex) + ":\n" + actionInfo[0]
                except:
                    pass
                
                # Each action is run according to its mode
                if actionInfo[0] == "Retrieve":
                    self.runRetrieve(actionInfo[1][0], actionInfo[1][1], actionInfo[1][2])
                elif actionInfo[0] == "Dispense":
                    self.runDispense(actionInfo[1][0], actionInfo[1][1], actionInfo[1][2])
                elif actionInfo[0] == "Back-and-Forth":
                    self.runBackAndForth(actionInfo[1][0], actionInfo[1][1], actionInfo[1][2], actionInfo[1][3])
                else:
                    self.runRecycle(actionInfo[1][0], actionInfo[1][1], actionInfo[1][2], actionInfo[1][3], actionInfo[1][4])
                
    # Sets the display text in the user interface to "Task Completed" to let the user know that the task is completed
    def taskCompleted(self):
        try:
            self.executionTextObject.text = "Task Completed"
        except:
            pass
        
    # Stops the current task be terminating the current command buffer and ending any task or action loops
    # Also changes the display text in the user interface to "Task Stopped" to let the user know that the task was stopped
    def stopTask(self):
        self.looper.stop() #Stops taskLoop
        try:
            self.updater.stop() #Stops the loop in any individual action if currently active
        except:
            pass
        try:
            self.ser.write("/1T\r".encode()) #Sends a "terminate command buffer" command to the pump
        except:
            pass
        self.executionTextObject.text = "Task Stopped"
    
    # Runs Initialization on the Pump
    def runInitialization(self):
        self.ser.write('/1YR\r'.encode()) #Sends initialization command
        self.ser.readline()
        
        self.actionActive = True #Action Active
        self.updater = ThreadUpdater(self.basicActionUpdate, 0.1) #Runs basicActionUpdate every 0.1 seconds
        self.updater.start()
        
    # Runs the Retrieve Command on the Pump
    def runRetrieve(self, valve, volume, speed):
        command = '/1S' + str(speed) + 'I' + str(valve) + 'P' + str(volume) + 'R\r' #Runs retrieve command
        self.ser.write(command.encode())
        self.ser.readline()
        
        self.actionActive = True #Action Active
        self.updater = ThreadUpdater(self.basicActionUpdate, 0.1) #Runs basicActionUpdate every 0.1 seconds
        self.updater.start()
        
    # Runs the Dispense Command on the Pump
    def runDispense(self, valve, volume, speed):
        command = '/1S' + str(speed) + 'O' + str(valve) + 'D' + str(volume) + 'R\r' #Runs dispense command
        self.ser.write(command.encode())
        self.ser.readline()
        
        self.actionActive = True
        self.updater = ThreadUpdater(self.basicActionUpdate, 0.1) #Runs basicActionUpdate every 0.1 seconds
        self.updater.start()
        
    # An Update Function Called to Check if a One-Step Action is Completed
    # Once the action is completed, the loop stops and self.actionActive is set to False
    def basicActionUpdate(self):
        try:
            self.ser.write('/1Q\r'.encode()) #Sends a query command to the pump
            query = self.ser.readline()
        except: #If unable to send query, the task is stopped and the user is given an error message
            self.stopTask()
            self.executionTextObject.text = "Could Not Connect\nTo Device"
        try:
            query = query.decode()
        except:
            query = '  @'
        
        if query == "": #No response receieve
            self.stopTask()
            self.executionTextObject.text = "Could Not Connect\nTo Device"
        elif query[2] != '@': #Pump is no longer received, so we know that the action has ended
            self.updater.stop()
            self.actionActive = False
    
    # Runs the Back and Forth Action on the Pump
    def runBackAndForth(self, valve, volume, speed, length):
        self.initialTime = time() #Gets the current time
        self.actionLength = length #Sets length
        self.actionParameters = [valve, volume, speed] #Sets parameters to be used during execution
        self.actionActive = True #Action Active
        
        self.updater = ThreadUpdater(self.backAndForthUpdate, 0.1) #Runs backAndForthUpdate every 0.1 seconds to continue the action
        self.updater.start()
        
    # Update Function that is called to run the Back-and-Forth command again when completed, until the length of the action passes
    def backAndForthUpdate(self):
        if(time() > self.initialTime + self.actionLength): #When the time elapsed is greater than the length of the action
            self.updater.stop() #Task is stopped
            self.updater = ThreadUpdater(self.basicActionUpdate, 0.1) #Starts basicActionUpdate to wait until the current command is completed
            self.updater.start()
        else: #There is still time left
            try:
                self.ser.write('/1Q\r'.encode()) #Write query command to pump
                query = self.ser.readline()
            except: #Could not write to device, so task is stopped
                self.stopTask()
                self.executionTextObject.text = "Could Not Connect\nTo Device"
            try:
                query = query.decode()
            except:
                query = '  @'
            if query == "": #If reponse is empty, the task is stopped
                self.stopTask()
                self.executionTextObject.text = "Could Not Connect\nTo Device"
            elif query[2] != '@': #Otherwise, another Back-and-Forth command is issued
                valve  = self.actionParameters[0]
                volume = self.actionParameters[1]
                speed = self.actionParameters[2]
                
                command = '/1S' + str(speed) + 'O' + str(valve) + 'D' + str(volume) + 'P' + str(volume) + 'R\r'
                self.ser.write(command.encode())
                self.ser.readline()
    
    # Runs the Recycle Action on the Pump
    def runRecycle(self, valve, volume, speed, length, recycleValve):
        self.initialTime = time() #Gets the current time
        self.actionLength = length #Sets length
        self.actionParameters = [valve, volume, speed, recycleValve] #Starts basicActionUpdate to wait until the current command is completed
        self.actionActive = True #Action Active
        
        self.updater = ThreadUpdater(self.recycleUpdate, 0.1) #Runs recyleUpdate every 0.1 seconds to continue the action
        self.updater.start()
        
    # Update Function that is called to run the Recycle command again when completed, until the length of the action passes
    def recycleUpdate(self):
        if(time() > self.initialTime + self.actionLength): #When the time elapsed is greater than the length of the action
            self.updater.stop() #Task stopped
            self.updater = ThreadUpdater(self.basicActionUpdate, 0.1)
            self.updater.start()
        else: #There is still time left
            try:
                self.ser.write('/1Q\r'.encode()) #Write query command to pump
                query = self.ser.readline()
            except: #Could not write to device, so task is stopped
                self.stopTask()
                self.executionTextObject.text = "Could Not Connect\nTo Device"
            try:
                query = query.decode()
            except:
                query = '  @'
            if query == "": #If reponse is empty, the task is stopped
                self.stopTask()
                self.executionTextObject.text = "Could Not Connect\nTo Device"
            elif query[2] != '@': #Otherwise, another Recycle command is issued
                valve = self.actionParameters[0]
                volume = self.actionParameters[1]
                speed = self.actionParameters[2]
                recycleValve = self.actionParameters[3]
        
                command = '/1S' + str(speed) + 'O' + str(valve) + 'D' + str(volume) + 'I' + str(recycleValve) + 'P' + str(volume) + 'R\r'
                self.ser.write(command.encode())
                self.ser.readline()

    
SerialManager = SerialManager()