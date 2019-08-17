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
        print("New Default File Path: ", self.file_path)
    
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
            print("No File Given")
            return None
        try:
            with open(file_path) as file:
                selectedFile = json.load(file)
                print(self.file_name, "Loaded Succesfully @ ", file_path)
                return selectedFile
        except FileNotFoundError:
            print("File Not Found @ ", file_path)
            return None
        except:
            print("File not in correct format.")
            return None
    #goes through an encoded list of strings and numbers (ex:Z1R) to produce a list readable in the interface
    def parseString(self, input_string):
        #the dictionary of all commands after they're converted into readable format
        actions = []
        #a running variable that stores all numbers following a letter command
        current_int = ""
        print("String to parse: ", input_string)
        list_of_lists = []
        
        for index in range(1, len(input_string)+1):
    
            try:
                x = input_string[str(index)][1][3]
            except IndexError:
                input_string[str(index)][1].append(0)
            
            try:
                x = input_string[str(index)][1][4]
            except IndexError:
                input_string[str(index)][1].append(0)
                
            if input_string[str(index)][0] == "Retrieve":
                param = "I Valve: " + str(input_string[str(index)][1][0]) + " Vol: " + str(input_string[str(index)][1][1]) + " Speed: " + str(input_string[str(index)][1][2])
            elif input_string[str(index)][0] == "Dispense":
                param = "O Valve: " + str(input_string[str(index)][1][0]) + "Vol: " + str(input_string[str(index)][1][1]) + " Speed: " + str(input_string[str(index)][1][2])
            elif input_string[str(index)][0] == "Recycle":
                param = "O Valve: " + str(input_string[str(index)][1][0]) + " Vol: " + str(input_string[str(index)][1][1]) + " Speed: " + str(input_string[str(index)][1][2]) + " Time: " + str(input_string[str(index)][1][3]) + "Bypass: " + str(input_string[str(index)][1][4])
            elif input_string[str(index)][0] == "Back-and-Forth":
                param = "Valve: " + str(input_string[str(index)][1][0]) + " Time: " + str(input_string[str(index)][1][1]) + " Vol: " + str(input_string[str(index)][1][2]) + " Speed: " + str(input_string[str(index)][1][3])
 
            list_of_lists.append([(str(index) + ": " + input_string[str(index)][0]), param])
        
        
        return list_of_lists
    
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
            print("File Successfully Saved: ", self.dict_to_save)
FileManager = FileManager()