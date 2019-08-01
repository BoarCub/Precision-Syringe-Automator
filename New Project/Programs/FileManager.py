import os
import json

class FileManager(object):
    def __init__(self):
        #contains all of the commands with their corresponding 'one letter' ids
        self.all_commands = self.importFile(
            self.shortenFilePath(os.path.dirname(os.path.realpath(__file__)))+ "/Databases/CommandsDatabase")
        
        #contains the reverse of 'all_commands' to allow         
        self.rev_commands = self.reverseDictionary(self.all_commands)
    
    def importFile(self, file_path): #imports file using json
        if file_path == None:
            print("No File Given")
            return None
        try:
            with open(file_path) as file:
                selectedFile = json.load(file)
                print("File Loaded Succesfully @ ", file_path)
                return selectedFile
        
        except FileNotFoundError:
            print("File Not Found @ ", file_path)
            return None
        
        except:
            print("File Not Imported @ ", file_path)
            return None
        
    #deletes the last location in a file path (ex: C:/Users/Aniket -> C:/Users/)
    def shortenFilePath(self, file_path):
        #counts the number of times a slash is found
        for index in range ((len(file_path)-1), 0, -1):
            if file_path[index] == "/" or file_path[index] == "\\":
                break
            
        file_path = file_path[0:index]
        return file_path
    
    #reverses the keys and values of a dictionary
    def reverseDictionary(self, inputlist):
        newDict = {}
        for key in inputlist:
            #assign the same spot in a placebo dictionary that assigns the key as value and vice versa
            newDict.update({inputlist[key]: key})
            
        return newDict
            
filemanager_object = FileManager()
print(filemanager_object.rev_commands)