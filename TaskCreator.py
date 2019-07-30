class TaskCreator(object):
    def __init__(self):
        self.mode = "Output"
        self.action = ""
        self.num = 1
    def takeMode(self, value):
        print(value)
        self.mode = value
    def takeAction(self, value):
        print(value)
        self.action = value
    def takeNum(self, value):
        print(value)
        self.num = value
taskcreator_object = TaskCreator()