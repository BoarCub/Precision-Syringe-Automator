import os
import json

class FileManager(object):
    def __init__(self):
        #contains the name (ex: CommandsDatabas) of the current file being imported
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
                
        if file_path == None:
            print("No File Given")
            return None
        
        with open(file_path) as file:
            selectedFile = json.load(file)
            print(self.file_name, "Loaded Succesfully @ ", file_path)
            return selectedFile
        
        
    
    #goes through an encoded list of strings and numbers (ex:Z1R) to produce a list readable in the interface
    def parseString(self, input_string):
        #the list of all commands after they're converted into readable format
        actions = []
        #a running variable that stores all numbers following a letter command
        current_int = ""
        print("String to parse: ", input_string)
        for char_index in range(len(input_string)):
            #if the current highlighted character is a letter
            if (input_string[char_index].isalpha()):
                #the current action is the command corresponding the letter in the reverse commands dictionary (ex: "R": "Execute Command Buffer)
                current_action = self.rev_commands[input_string[char_index]]
                #clear the running number variable because we're about to recieve a new one corresponding to a command
                current_int = ""
                
            #if the current character is a number, add it to the current runnnig variable (current_int)
            elif (input_string[char_index].isdigit()):
                current_int += input_string[char_index]
                
            else: print("Command is in incorrect format.")
            
            #if the next character in the list is a letter, that indicates that the current command's details are over
            try:
                if(input_string[char_index+1].isalpha()):
                    actions.append([current_action, current_int])
            
            #The Try and Except exists because the current character may be the last one; in that case, add the current action to list 'actions'
            except IndexError:
                actions.append([current_action, current_int])
                

        return actions
    
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
            
FileManager = FileManager()