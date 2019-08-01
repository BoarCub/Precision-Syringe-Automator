class SerialManager(object):
    def __init__(self):
        print( )
    
    #receives input in the format [[title_of_function, value], etc.] and converts it to serial code (ex: Y1R)
    def encodedCommands(self, nested_lists):
        #The entire string of commands (ex: Y1R)
        command = ""
        for small_list in nested_lists:
            #the letter corresponding to title_of_function
            current_action = small_list[0]
            current_num = small_list[1]
            command += self.all_commands[current_action] + current_num
        print("Converted ", nested_lists, "to ", command)
        return command
