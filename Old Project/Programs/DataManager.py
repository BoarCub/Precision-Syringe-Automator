import json
import os
class FileImporter:
    
    def __init__ (self):
        self.filePath = None
        self.all_commands = self.getCommands()
        self.rev_commands = self.reverseDictionary(self.all_commands)
        self.actions = []
        self.displayedActions = None
        self.command_values = self.getValues()


    def setPath(self, path):
        self.filePath = path
    def userCommands(self):
        newList = []
        for key in self.all_commands.keys():
            newList.append(key)
        return newList
    def getValues(self):
        try:
            with open(self.makeBroaderPath(os.path.dirname(os.path.realpath(__file__))) + "/Databases/ValuesDatabase") as file:
                self.command_values =  json.load(file)
            return self.command_values
        except FileNotFoundError:
            print("Value Database file not found.")

    def checkValue(self, pair):
        if (len(self.command_values[pair[0]]) == 0):
            if(pair[1] == None):
                return True
            else:
                return False
        elif (self.command_values[pair[0]] != [] or self.command_values[pair[0]] != None):
            min = self.command_values[pair[0]][0]
            max = self.command_values[pair[0]][1]
            if (pair[1] != None and pair[1]<=max and pair[1]>=min):
                return True
            else: return False
        else:
            if pair[1] == None:
                return True
            else:
                return False
    def reverseDictionary(self, inputlist): #reverses the dictionary of commands so we can search by both action and command
        newDict = {}
        for colorString in inputlist: #for ever value in the dictionary
            newDict.update({inputlist[colorString]: colorString}) #assign the same spot in a placebo dictionary that assigns the key as value and vice versa
        return newDict
        
    def importFile(self): #uses json to import the string stored in the file
        
        if self.filePath == None:
            print("no file")
            return None
        try:
            with open(self.filePath) as file:
                selectedRoutine = json.load(file)
                print("able to read file")
                return selectedRoutine
        except:
            print("file not compatible")
            return None
        
    def getCommands(self): #returns the entire file using json
        try: #self.makeBroaderPath(os.path.dirname(os.path.realpath(__file__))) +
            with open(self.makeBroaderPath(os.path.dirname(os.path.realpath(__file__)))+ "/Databases/CommandsDatabase") as file:
                self.all_commands =  json.load(file)
            return self.all_commands

        except FileNotFoundError:
            print(self.makeBroaderPath(os.path.dirname(os.path.realpath(__file__))))
            print("Command Database file not found.")

    def makeBroaderPath(self, file_path):
        dash_index = 0
        for index in range ((len(file_path)-1), 0, -1):
                if file_path[index] == "/" or file_path[index] == "\\":
                    dash_index = index
                    break
        file_path = file_path[0:index]
        return file_path
    def encodedCommands(self, big_list):
        command = ""
        current_action = ""
        current_num = 0
        for small_list in big_list:
            current_action = small_list[0]
            current_num = small_list[1]
            command += self.all_commands[current_action] + current_num
        print(command)
        return command
    def parseImportedString(self, stringToParse): #goes through every character in a given string and separates command with their associated numbers
        self.actions = []
        current_action = ""
        current_int = ""
        for char_index in range(len(stringToParse)):
            #print(char_index, ": ", stringToParse[char_index])
            if (stringToParse[char_index].isalpha()):
                #print("isalpha")
                current_action = self.rev_commands[stringToParse[char_index]]
                current_int = ""
            elif (stringToParse[char_index].isdigit()):
                #print("isdigit")
                current_int += stringToParse[char_index]
            else: print("Command is in incorrect format")
            
            try:
                if(stringToParse[char_index+1].isalpha()):
                    self.actions.append([current_action, str(current_int)])
                    #print("appending command")
            except IndexError:
                self.actions.append([current_action, str(current_int)])
                #print("appending command through except")
        #print(self.actions)
        return self.actions
            
FileImporter = FileImporter()
#FileImporter.parseImportedString("Z2O86G6O1")
#print(FileImporter.checkValue(["R", 150]))