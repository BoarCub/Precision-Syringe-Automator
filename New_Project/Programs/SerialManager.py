from FileManager import *
from ThreadManager import *
from time import sleep
from time import time
import serial
import serial.tools.list_ports

class SerialManager(object):
    def __init__(self):
        #contains a dictionary of commands based on step (ex: {1: [IAR]})
        self.commands_dict = {}
        #contains the action in order of step (ex: {1: "Dispense"}
        self.actions_dict = {}
        #contains a list of queries and their potential repsonses
        self.query_database = FileManager.importFilePath(
            FileManager.shortenFilePath(os.path.dirname(os.path.realpath(__file__)))+ "/Databases/QueryDatabase")
        
        self.index = 0
        
        #The below VID (Vendor ID) and PID (Product ID) constants are set by the manufacturer and are used to identify the USB Device
        self.VID = 1659
        self.PID = 8963
        
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
    
    def statusMessage(self, status):
        message = ""
        error_code = status[1]
        if status[0] == 1:
            message += "Ready; "
        else:
            message += "Busy; "
        if str(error_code) == "@" or str(error_code)== "‘":
            message =+ "No error."
        elif lower(str(error_code)) == "a":
            message =+ "Initialization error."
        elif lower(str(error_code)) == "b":
            message =+ "Invalid command."
        elif lower(str(error_code)) == "c":
            message =+ "Invalid operand/parameter."
        elif lower(str(error_code)) == "d":
            message =+ "Invalid command sequence."
        elif lower(str(error_code)) == "g":
            message =+ "Syringe not initialized."
        elif lower(str(error_code)) == "i":
            message =+ "Syringe Pressure Overload."
        elif lower(str(error_code)) == "j":
            message =+ "Valve Pressure Overload."
        elif lower(str(error_code)) == "k":
            message =+ "Syringe move not allowed (valve in bypass or throughput)."
        elif lower(str(error_code)) == "o":
            message =+ "Pump is busy."
    
    # Turns a string of ascii characters into a list of bitsb
    def tobits(self, string):
        result = []
        for c in string:
            bits = bin(ord(c))[2:]
            bits = '00000000'[len(bits):] + bits
            result.extend([int(b) for b in bits])
        
        return result

    # Turns a list of bits into a string of ascii characters
    def frombits(bits):
        chars = []
        for b in range(int(len(bits) / 8)):
            byte = bits[b*8:(b+1)*8]
            chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    
        return ''.join(chars)

    # Returns a checksum as a single ascii character given a list of ascii characters, representing the command
    def calculateChecksum(commandsList):
        
        bitsList = []
        
        for command in commandsList:
            bitsList.append(tobits(command))
            
        sum = bitsList[0]

        for pos in range (0, 8):
            for i in range(1, len(commandsList)):
                sum[pos] += bitsList[i][pos]
                
        for i in range (0, 8):
            sum[i] = sum[i] % 2
            
        return frombits(sum)
    
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
            query = query.decode()[2]
        except:
            query = '@'
        
        if query != '@':
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
                query = query.decode()[2]
            except:
                query = '@'
        
            if query != '@':        
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
                query = query.decode()[2]
            except:
                query = '@'
                
            if query != '@':
                valve = self.actionParameters[0]
                volume = self.actionParameters[1]
                speed = self.actionParameters[2]
                bypassValve = self.actionParameters[3]
        
                command = '/1S' + str(speed) + 'O' + str(valve) + 'D' + str(volume) + 'I' + str(bypassValve) + 'P' + str(volume) + 'R\r'
                self.ser.write(command.encode())
                self.ser.readline()
        
    def queryToString(self, query, response):
        message = ""
    
        if (query == "?10000"):
            zero1 = "Syringe intialized "
            one = "Syringe not initialized. "
            six = "Syringe stalled. "
            zero2 = "No syringe stall or overload. "
            eight = "Syringe intialization error. "
            zero3 = "No initialization error. "
            if response == 0:
                message = zero1 + zero2 + zero3
            elif response == 1:
                message = one + zero2 + zero3
            elif response == 6:
                message = zero1 + six + zero3
            elif response == 8:
                message = zero1 + zero2 + eight
                
            elif response == 7:
                message = one + six + zero3
            elif response == 9:
                message = one + zero2 + eight
            elif response == 14:
                message = zero1 + six + eight
            elif response == 15:
                message = one + six + eight
            else:
                print(response, " isn't recognized under query ", query)
                return None
        elif (query == "?10001"):
            if response == 1:
                message = "Syringe in home region."
            elif response == 0:
                message = "Syringe not in home region."
            else:
                print(response, " isn't recognized under query ", query)
                return  None
        elif (query == "?11000"):
            zero1 = "Standard mode set. "
            one = "High resolution mode set. "
            two = "Syringe overload ignored. "
            zero2 = "Syringe overload not ignored. "
            four = "Disable initialization error. "
            zero3 = "Enable initialization error. "
            eight = "Disable initialize. "
            zero4 = "Enable Initialize. "
            if response == 0:
                message = zero1 + zero2 + zero3 + zero4
            elif response == 1:
                message = one + zero2 + zero3 + zero4
            elif response == 2:
                message = zero1 + two + zero3 + zero4
            elif response == 4:
                message = zero1 + zero2 + four + zero4
            elif response == 8:
                message = zero1 + zero2 + zero3 + eight
                
            elif response == 3:
                message = one + two + zero3 + zero4
            elif response == 5:
                message = one + zero2 + four + zero4 
            elif response == 9:
                message = one + zero2 + zero3 + eight
            elif response == 10:
                message = zero1 + two + zero3 + eight
            elif response == 12:
                message == zero1 + zero2 + four + eight
            elif response == 6:
                message == zero1 + two + four + zero4
            
            elif  response == 11:
                message = one + two + zero3 + eight
            elif response == 13:
                message == one + zero2 + four + eight
            elif response == 7:
                message == one + two + four + zero4
            else:
                print(response, " isn't recognized under query ", query)
                return  None
        elif (query == "?20000"):
            zero1 = "Valve initialized. "
            one = "Valve not initialized. "
            zero2 = "No Valve initialization error. "
            two = "Valve initialization error. "
            zero3 = "No valve stall. "
            four = "Valve stall. "
            zero4 = "Valve enabled. "
            sixteen = "Valve not enabled. "
            zero5 = "Valve is not busy. "
            thirty_two = "Valve is busy. "
            if response == 0:
                message = zero1 + zero2 + zero3 + zero4 + zero5
            elif response == 1:
                message == one + zero2 + zero3 + zero4 + zero5
            elif response == 2:
                message = zero1 + two + zero3 + zero4 + zero5
            elif response == 4:
                message = zero1 + zero2 + four + zero4 + zero5
            elif response == 16:
                message  =zero1 + zero2 + zero3 + sixteen + zero5
            elif response == 32:
                message = zero1 + zero2 + zero3 + zero4 + thirty_two
                
            
            elif response == 3:
                message = one + two + zero3 + zero4 + zero5
            elif response == 5:
                message == one + zero2 + four + zero4 + zero5
            elif response == 17:
                message = one + zero2 + zero3 + sixteen + zero5
            elif response == 33:
                message = one + two + four + zero4 + zero5
                
            elif response == 6:
                message = zero1 + two + four + zero4 + zero5
            elif response == 18:
                message = zero1 + two + zero3 + sixteen + zero5
            elif response == 34:
                message = zero1 + two + zero3 + zero4 + thirty_two
            elif response == 20:
                message = zero1 + zero2 + four + sixteen + zero5
            elif response == 36:
                message= zero1 + zero2 + four + zero4 + thirty_two
                
            elif response == 52:
                message = zero1 + zero2 + zero3 + sixteen + thirty_two
                
                
            elif response == 7:
                message = one + two + four + zero4 + zero5
            elif response == 19:
                message = one + two + zero3 + sixteen + zero5
            elif response == 35:
                message = one + two + zero3 + zero4 + thirty_two
                
            elif response == 21:
                message = one + zero2 + four + sixteen + zero5
            elif response == 37:
                message = one + zero2 + four + zero4 + thirty_two
                
            elif response == 53:
                message = one + zero2 + zero3 + sixteen + thirty_two
                
                
            elif response == 22:
                message = zero1 + two + four + sixteen + zero5
            elif response == 38:
                message = zero1 + two + four + zero4 + thirty_two
                
            elif response == 54:
                message = zero1 + two + zero3 + sixteen + thirty_two
                
            elif response == 75:
                message = one + two + four + sixteen + thirty_two
            else:
                print(response, " isn't recognized under query " ,query)
                return  None
        elif (query == "?23000"):
            if response == 0:
                message = "Not at logical position. "
            elif repsonse == 1:
                message = "Input"
            elif response == 2:
                message = "Output"
            elif response == 3:
                message = "Wash"
            elif response == 4:
                message = "Return"
            elif response == 5:
                message = "Bypass"
            elif response == 6:
                message = "Extra"
            else:
                print(response, " isn't recognized under query " ,query)
                return  None    
        elif (query == "?24000"):
            message = response
        elif (query == "?25000"):
            message = response
        return message
    
SerialManager = SerialManager()