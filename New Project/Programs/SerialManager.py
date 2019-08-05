class SerialManager(object):
    def __init__(self):
        #contains a dictionary of commands based on step (ex: {1: [IAR]})
        self.command_list = {}
        #contains the action in order of step (ex: {1: "Dispense"}
        self.action_list = {}
    
    #receives input in the format [[title_of_function, value], etc.] and converts it to serial code (ex: Y1R)
    def encodeCommands(self, input_dictionary):
        print(input_dictionary)
            
        for index in range(0, len(input_dictionary)):
            print(index)
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
                current_step = ["S" + str(speed) + "O" + str(output_valve) + "D" + str(volume)]
                self.action_list[index] = ["Dispense", time]
                
            elif (input_dictionary[index+1][0] == "Retrieve"):
                input_valve = current_param_list[0]
                volume = current_param_list[1]
                speed = current_param_list[2]
                current_step = ["S" + str(speed) + "I" + str(input_valve) + "P" + str(volume)]
                self.action_list[index] = ["Retrieve", time]
                
            elif (input_dictionary[index+1][0] == "Recycle"):
                output_valve = current_param_list[0]
                return_valve = current_param_list[1]
                volume = current_param_list[2]
                time = current_param_list[3]
                speed = current_param_list[4]
                self.action_list[index] = ["Recycle", time]
                current_step = ["S" + str(speed) + "O" + str(output_valve) + "D" + str(volume) + "P" + str(return_valve)]
                
            elif (input_dictionary[index+1][0] == "Back+Forth"):
                valve = current_param_list[0]
                time = current_param_list[1]
                volume = current_param_list[2]
                speed = current_param_list[3]
                self.action_list[index] = ["Back+Forth", time]
                current_step = ["S" + str(speed) + "O" + str(valve) + "D" + str(volume) + "I" + str(valve) + "P" + str(volume)]
                 
            self.command_list[index+1] = current_step             
    
    def setCommands(self, commands):
        command_list = command
        
SerialManager = SerialManager()
SerialManager.encodeCommands({1: ["Dispense", [8, 10, 5]], 2: ["Recycle", [8, 1, 300, 4, 5]]})
print(SerialManager.command_list)
print(SerialManager.action_list)