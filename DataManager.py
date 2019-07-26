import json
import os
class FileImporter:
    
    def __init__ (self):
        self.filePath = None
        
    def setPath(self, path):
        self.filePath = path
        
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
            with open(os.path.dirname(os.path.realpath("C:\Users\Aniket\Documents\CommandDatabase"))) as file:
                all_commands = hjson.load(file)
            return all_commands
        except FileNotFoundError:
            print("Command Database file not found.")
FileImporter = FileImporter()
print(FileImporter.getCommands())
