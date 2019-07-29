import json
import os
class FileImporter:
    
    def __init__ (self):
        self.filePath = None
        self.all_commands = {}
        self.getCommands()
        self.rev_commands = self.reverseDictionary(self.all_commands)
        self.actions = []
        
    def setPath(self, path):
        self.filePath = path

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
        try:
            with open("/home/pi/Precision-Syringe-Automator" + "/CommandsDatabase") as file:
                self.all_commands =  json.load(file)
            return self.all_commands

        except FileNotFoundError:
            print("Command Database file not found.")
            
    def parseImportedString(self, stringToParse): #goes through every character in a given string and separates command with their associated numbers
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