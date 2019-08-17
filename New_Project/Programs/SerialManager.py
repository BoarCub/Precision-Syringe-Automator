from FileManager import *
from ThreadManager import *
from time import sleep
import serial
from TaskManager import *

class SerialManager(object):
    def __init__(self):
        #contains a dictionary of commands based on step (ex: {1: [IAR]})
        self.commands_dict = {}
        #contains the action in order of step (ex: {1: "Dispense"}
        self.actions_dict = {}
        #contains a list of queries and their potential repsonses
        self.query_database = FileManager.importFilePath(
            FileManager.shortenFilePath(os.path.dirname(os.path.realpath(__file__)))+ "/Databases/QueryDatabase")
        
        self.updater = ThreadUpdater(self.run, 1)
        #self.updater.run()
        
        self.index = 0
        
        self.ser = serial.Serial('COM9', 9600, timeout =5)
        self.shouldRepeat = True
        self.response = ""
        
    def sendMessage(self, message):
        print(TaskManager.newTaskActions)
        self.ser.write(b'/1Z' + message.encode() + b'R\r')
        sleep(0)
        
        while True:
            self.response = self.ser.readline().decode()      
            print("response: ", self.response)
            if self.response != "":
                break
    def run(self):
        pass
    
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
        
    def checkReady(self):
        self.sendMessage("Q")
        if self.response[2] == "`":
            print("Ready")
            return True
        print("Not Ready")
        return False
    
    def readLine(self):
        print("readLine: 0")
        return 0
    
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
    
    def writeToLine(self, command):
        print("writeLine: ", command)
    
    #receives input in the format [[title_of_function, value], etc.] and converts it to serial code (ex: Y1R)
    def encodeCommands(self, input_dictionary):
        print("input: ", input_dictionary)
        output_dictionary = {}
        for index in range(0, len(input_dictionary)):
            current_step = []
            time = 0
            current_param_list = input_dictionary[index+1][1]
            #avoids IndexError because some commands don't take a 4th index parameter
            try:
                if current_param_list[3] != None:
                    print()
                
            except IndexError:
                current_param_list.append(0)
                
            #same thing for 5th index
            try:
                if current_param_list[4] != None:
                    print()
                
            except IndexError:
                current_param_list.append(0)
            
            if (input_dictionary[index+1][0] == "Dispense"):
                output_valve = current_param_list[0]
                volume = current_param_list[2]
                speed = current_param_list[3]
                current_step = "S" + str(speed) + "O" + str(output_valve) + "D" + str(volume)
                self.actions_dict[index+1] = ["Dispense", time]
                
            elif (input_dictionary[index+1][0] == "Retrieve"):
                input_valve = current_param_list[0]
                volume = current_param_list[1]
                speed = current_param_list[2]
                current_step = "S" + str(speed) + "I" + str(input_valve) + "P" + str(volume)
                self.actions_dict[index+1] = ["Retrieve", time]
                
            elif (input_dictionary[index+1][0] == "Recycle"):
                output_valve = current_param_list[0]
                return_valve = current_param_list[1]
                volume = current_param_list[2]
                time = current_param_list[3]
                speed = current_param_list[4]
                self.actions_dict[index+1] = ["Recycle", time]
                current_step = "S" + str(speed) + "O" + str(output_valve) + "D" + str(volume) + "P" + str(return_valve)
                
            elif (input_dictionary[index+1][0] == "Back-and-Forth"):
                valve = current_param_list[0]
                time = current_param_list[1]
                volume = current_param_list[2]
                speed = current_param_list[3]
                self.actions_dict[index+1] = ["Back-and-Forth", time]
                current_step = "S" + str(speed) + "O" + str(valve) + "D" + str(volume) + "I" + str(valve) + "P" + str(volume)
                 
            output_dictionary[index+1] = current_step
        print("output: ", output_dictionary)
        self.commands_dict = output_dictionary
        return output_dictionary
    
    def setCommands(self, commands):
        command_list = command
        
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
SerialManager.checkReady()