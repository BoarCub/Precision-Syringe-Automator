# Task Manager handles the data and processing of tasks and actions
class TaskManager(object):
    
    def __init__ (self):
        
        # Holds all of the actions in a newly created task
        # Follows this format {"# of Task Starting from 1": [# of Input Valve, # of Output Valve, "Mode (Time or Volume)", # of Value, # of Speed]
        self.newTaskActions = {}
        self.taskRows = []
        
    def checkNone(self):
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
    
    # Deletes a Task at a specific index and shift everything else down
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
            if action == "Recycle":
                message = "Cycling " + str(parameters[1]) + " steps at speed " + str(parameters[2]) + "/40, to valve, " + str(parameters[0]) + "\nand returning through valve, " + str(parameters[4]) + " for " + str(parameters[3]) + " seconds"
        except IndexError:            
            pass
        if action == "Dispense":
            message = "Dispensing " + str(parameters[1]) + " steps, at speed " + str(parameters[2]) + "/40,\nout of valve " + str(parameters[0])
        if action == "Retrieve":
            message = "Retrieving " + str(parameters[1]) + " steps, at speed " + str(parameters[2]) + "/40,\ninto valve, " + str(parameters[0])
        return message
    
    def checkParameters(self, action_list):
        action = action_list[0]
        parameters = action_list[1]
        
        for parameter in parameters:
            if parameter == None:
                return False
        
        if action == "Dispense":
            if parameters[0] > 8 or parameters[0] <1:
                return False
            if parameters[1] <= 0 or parameters[1] >3000:
                return False
            if parameters[2] <=0 or parameters[2] > 40:
                return False
        if action == "Retrieve":
            if parameters[0] > 8 or parameters[0] <1:
                return False
            if parameters[1] <= 0 or parameters[1] >3000:
                return False
            if parameters[2] <=0 or parameters[2] > 40:
                return False
        if action == "Recycle":
            if parameters[0] > 8 or parameters[0] <1:
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
            if parameters[0] > 8 or parameters[0] <1:
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