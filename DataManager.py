import json

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
        
FileImporter = FileImporter()