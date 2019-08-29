# Task Manager handles the data and processing of tasks and actions
class TaskManager(object):
    
    def __init__ (self):
        
        # Holds all of the actions in a newly created task or imported task
        # Also referred to as the running task dictionary
        # Follows this format {"# of Task Starting from 1": [Mode (Retrieve, Dispense, Back-and-Forth or Continuous Dispense), [# of Valve, Volume from 1-3000, Speed from 1-40 (1 fastest, 40 slowest), Time in seconds (only needed for Back-and-Forth and Continuous Dispense), Extra Valve (Only Needed for Back-and-Forth)]] }
        self.newTaskActions = {}
        
        # A list holding all of the layouts for each action row in the user interface
        # List is ordered, starting with row 1
        # Each row corresponds to an action in self.newTaskActions
        self.taskRows = []
        
    # Checks if any steps in the task extend the syringe too much
    # Returns False if within bounds
    # Returns a string with the specific error information otherwise
    def checkOutOfBounds(self):
        try:
            position = 0
            
            for i in range(1, len(self.newTaskActions)+1):
                action = self.newTaskActions[str(i)]
                
                if action[0] == "Retrieve":
                    position += action[1][1]
                elif action[0] == "Dispense":
                    position -= action[1][1]
                else:
                    if position - action[1][1] < 0:
                        return "Not Enough Liquid Retrieved\nTo Execute Step " + str(i)
                    
                if position < 0:
                    return "Not Enough Liquid Retrieved\nTo Execute Step " + str(i)
                elif position > 3000:
                    return "Step " + str(i) + " Retrieves More\nLiquid Than Capacity"
                
            if position > 0:
                return "Not All Liquid Dispensed\nBy End of Task"
            
        except:
            return False
            
        return False
            
    # Returns a boolean representing whether the current task is completed filled (no empty actions)
    def checkNone(self):
        
        if len(self.newTaskActions) == 0:
            return False
        
        try:
            for newTaskAction in self.newTaskActions:
                if newTaskAction == None:
                    return False
            if self.newTaskActions == None:
                return False
            for index in range(1, len(self.newTaskActions)+1):
                current_parameters = self.newTaskActions[str(index)][1]
                for parameter in current_parameters:
                    if parameter == None:
                        return False
        except TypeError:
            return False
        return True
    
    # Deletes an action at a specific index and shift the other actions to fill the gap
    def deleteAction(self, index):
        try:
            for i in range(index, len(self.newTaskActions)):
                self.newTaskActions[str(i)] = self.newTaskActions[str(i+1)]
            del self.newTaskActions[str(len(self.newTaskActions))]
            del self.taskRows[index-1]
            
            for i in range(index-1, len(self.taskRows)):
                for widget in self.taskRows[i].children:
                    if(widget.id == "task_label"):
                        widget.text = str(int(widget.text)-1)
        except:
            self.newTaskActions = {}
            self.taskRows = []
    
    # Returns a short description of an action when given an action list
    # The action list parameter must be in the same format as the entries in newTaskActions
    def getDetails(self, action_list):
        message = ""
        action = action_list[0]
        parameters = action_list[1]
        try:
            if action == "Back-and-Forth":
                message = "Pulling and pushing " + str(parameters[1]) + " steps at speed " + str(parameters[2]) + "/40\nin valve " + str(parameters[0]) + " for " + str(parameters[3]) + " seconds"
        except IndexError:
            pass
        try:
            if action == "Continuous Dispense":
                message = "Cycling " + str(parameters[1]) + " steps at speed " + str(parameters[2]) + "/40, to valve, " + str(parameters[0]) + "\nand returning through valve, " + str(parameters[4]) + " for " + str(parameters[3]) + " seconds"
        except IndexError:            
            pass
        if action == "Dispense":
            message = "Dispensing " + str(parameters[1]) + " steps at speed " + str(parameters[2]) + "/40,\nout of valve " + str(parameters[0])
        if action == "Retrieve":
            message = "Retrieving " + str(parameters[1]) + " steps at speed " + str(parameters[2]) + "/40,\ninto valve, " + str(parameters[0])
        return message
    
    # Checks to see if a given action (as a list) is valid and returns True or False accordingly
    # The action list parameter must be in the same format as the entries in newTaskActions
    def checkParameters(self, action_list):
        action = action_list[0]
        parameters = action_list[1]
        
        for parameter in parameters:
            if parameter == None:
                return False
        
        if action == "Dispense":
            if parameters[0] > 6 or parameters[0] <1:
                return False
            if parameters[1] <= 0 or parameters[1] >3000:
                return False
            if parameters[2] <=0 or parameters[2] > 40:
                return False
        if action == "Retrieve":
            if parameters[0] > 6 or parameters[0] <1:
                return False
            if parameters[1] <= 0 or parameters[1] >3000:
                return False
            if parameters[2] <=0 or parameters[2] > 40:
                return False
        if action == "Continuous Dispense":
            if parameters[0] > 6 or parameters[0] <1:
                return False
            if parameters[1] <= 0 or parameters[1] >3000:
                return False
            if parameters[2] <=0 or parameters[2] > 40:
                return False
            if parameters[3] <= 0:
                return False
            if parameters[4] > 8 or parameters[0] <1:
                return False
        if action == "Back-and-Forth":
            if parameters[0] > 6 or parameters[0] <1:
                return False
            if parameters[1] <= 0 or parameters[1] >3000:
                return False
            if parameters[2] <=0 or parameters[2] > 40:
                return False
            if parameters[3] <= 0:
                return False
        return True            
        
        
# Creates a TaskManager object which can be used when the class is imported
TaskManager = TaskManager()