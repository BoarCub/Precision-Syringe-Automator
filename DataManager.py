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

    def reverseDictionary(self, inputlist):
        newDict = {}
        for colorString in inputlist:
            newDict.update({inputlist[colorString]: colorString})
        return newDict
        
    def importFile(self):
        
        if self.filePath == None:
            print("no file")
            return None
        try:
            with open(self.filePath) as file:
                selectedRoutine = json.load(file)
                print("able to read file")
                return (selectedRoutine)      
        except:
            print("file not compatible")
            return None
    def getCommands(self):
        try:
            with open(os.path.dirname(os.path.realpath(__file__)) + "/CommandsDatabase") as file:
                self.all_commands =  json.load(file)
            return self.all_commands

        except FileNotFoundError:
            print("Command Database file not found.")
            
    def parseImportedString(self, stringToParse):
        for char in range(0, len(stringToParse)):
            if stringToParse[char].isalpha():
                index = 1
                current_int = ""
                try:
                    while(stringToParse[char+index].isdigit()):
                        current_int += stringToParse[char + index]
                        self.actions.append(self.rev_commands[stringToParse[char]] + ": " + str(int(current_int))+", ")
                        index +=1
                except ValueError:
                    self.actions.append(self.rev_commands[stringToParse[char]]+", ")
                    pass
                except IndexError:
                    break
        print("actions are ", self.actions)
        return self.actions

            
FileImporter = FileImporter()
FileImporter.parseImportedString("Z2O86G6O1")

