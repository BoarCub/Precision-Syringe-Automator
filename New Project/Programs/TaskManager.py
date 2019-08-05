# Task Manager handles the data and processing of tasks and actions
class TaskManager(object):
    
    def __init__ (self):
        
        # Holds all of the actions in a newly created task
        # Follows this format {"# of Task Starting from 1": [# of Input Valve, # of Output Valve, "Mode (Time or Volume)", # of Value, # of Speed]
        self.newTaskActions = {}
        self.taskRows = []
        
# Creates a TaskManager object which can be used when the class is imported
TaskManager = TaskManager()