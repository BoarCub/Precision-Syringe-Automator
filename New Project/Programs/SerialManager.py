from kivy.clock import Clock
from FileManager import *
from ThreadManager import *
import time

class SerialManager(object):
    def __init__(self):
        #contains a dictionary of commands based on step (ex: {1: [IAR]})
        self.commands_dict = {}
        #contains the action in order of step (ex: {1: "Dispense"}
        self.actions_dict = {}
        #contains a list of queries and their potential repsonses
        self.query_database = FileManager.importFilePath(
            FileManager.shortenFilePath(os.path.dirname(os.path.realpath(__file__)))+ "/Databases/QueryDatabase")
        
        self.datetime = time.time()
        self.initialTime = self.datetime
        self.ThreadManager = ThreadUpdater(self.timeIt, 1)
        self.length = 0
        self.current_index = 0
        
    def timeIt(self):
        print(time.time())
        self.writeToLine(self.commands_dict[self.current_index])
        if (time.time() > self.initialTime + int(self.length)):
            self.ThreadManager.stop()
    def timeActions(self):
        for index in range(1, len(self.commands_dict)+1):
            if (self.actions_dict[index] == 0):
                self.writeToLine(self.commands_dict[index])
            else:
                self.current_index = index
                self.length = self.actions_dict[index]
                self.ThreadManager.run()
    def writeToLine(self, command):
        print("serial: ", command)
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
                self.actions_dict[index+1] = time
                
            elif (input_dictionary[index+1][0] == "Retrieve"):
                input_valve = current_param_list[0]
                volume = current_param_list[1]
                speed = current_param_list[2]
                current_step = "S" + str(speed) + "I" + str(input_valve) + "P" + str(volume)
                self.actions_dict[index+1] = time
                
            elif (input_dictionary[index+1][0] == "Recycle"):
                output_valve = current_param_list[0]
                return_valve = current_param_list[1]
                volume = current_param_list[2]
                time = current_param_list[3]
                speed = current_param_list[4]
                self.actions_dict[index+1] = time
                current_step = "S" + str(speed) + "O" + str(output_valve) + "D" + str(volume) + "P" + str(return_valve)
                
            elif (input_dictionary[index+1][0] == "Back-and-Forth"):
                valve = current_param_list[0]
                time = current_param_list[1]
                volume = current_param_list[2]
                speed = current_param_list[3]
                self.actions_dict[index+1] = time
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
SerialManager.encodeCommands({1: ["Recycle", [1, 1, 1, 5,1]], 2: ["Back and Forth", [2, 2, 2, 6]]})
SerialManager.timeActions()