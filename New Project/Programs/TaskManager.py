# Task Manager handles the data and processing of tasks and actions
class TaskManager(object):
    
    def __init__ (self):
        
        # Holds all of the actions in a newly created task
        # Follows this format {"# of Task Starting from 1": [# of Input Valve, # of Output Valve, "Mode (Time or Volume)", # of Value, # of Speed]
        self.newTaskActions = {}
        self.taskRows = []
        
    def checkNone(self):
        for index in range(1, len(self.newTaskActions)+1):
            current_parameters = self.newTaskActions[str(index)][1]
            for parameter in current_parameters:
                if parameter == None:
                    return False
        return True
    
    def getDetails(self, action_list):
        message = ""
        action = action_list[0]
        parameters = action_list[1]
        if action == "Dispense":
            message = "Dispensing " + str(parameters[1]) + " steps, at speed " + str(parameters[2]) + "/40, out of valve " + str(parameters[0])
        if action == "Retrieve":
            message = "Retrieving " + str(parameters[1]) + " steps, at speed " + str(parameters[2]) + "/40, into valve, " + str(parameters[0])
        if action == "Recycle":
            message = "Cycling " + str(parameters[1]), " steps at speed " + str(parameters[2]) + "/40, to valve, " + str(parameters[0]) + " and returning through valve, " + str(parameters[4]) + "for " + str(parameters[3]) + "seconds"
        if action == "Back-and-Forth":
            message == "Pulling and pushing " + str(parameters[1]) + " steps at speed " + str(parameters[2]) + "/40 in valve " + str(parameters[0]) + " for " + str(parameters[3]) + " seconds"
        
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
print(TaskManager.getDetails(["Dispense", [8, 30, 40]]))