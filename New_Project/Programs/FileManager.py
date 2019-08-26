import os
import json
from TaskManager import *

class FileManager(object):
    def __init__(self):
        #contains the name (ex: CommandsDatabase) of the current file being imported
        self.file_name = ""
        
        #contains all of the commands with their corresponding 'one letter' ids
        self.all_commands = self.importFilePath(
            self.shortenFilePath(os.path.dirname(os.path.realpath(__file__)))+ "/Databases/CommandsDatabase")
        #contains the reverse of 'all_commands' to allow         
        self.rev_commands = self.reverseDictionary(self.all_commands)
        
        #contains a current file_path in case a file_path is not known from the method in which this eing called
        self.file_path = ""
        
        #contains the current files being displayed after "Load File". Checking this variable prevent loading onto a previously displayed file
        self.displayed_actions = []
        
        self.dict_to_save = {}
        
    #sets the default file path used in importFile   
    def setPath(self, file_path):
        self.file_path = file_path
    
    #import the current self.file_path
    def importFile(self): 
        return self.importFilePath(self.file_path)
        
    #imports file using json
    def importFilePath(self, file_path):
        for index in range(len(file_path)-1, 0, -1):
            if (file_path[index]=="/" or file_path[index] == "\\"):
                self.file_name = file_path[index+1:len(file_path)]
                break
                
        if file_path == None or file_path == "":
            return None
        try:
            with open(file_path) as file:
                selectedFile = json.load(file)
                return selectedFile
        except FileNotFoundError:
            return None
        except:
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
    
    def writeFile(self, path, filename):
        self.dict_to_save = TaskManager.newTaskActions
        with open(os.path.join(path, filename), 'w') as file:
            json.dump(self.dict_to_save, file)
            
            
FileManager = FileManager()