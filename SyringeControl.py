class SyringeController(object):
    def __init__(self):
        self.ser = Serial('dev/ttyS0', 38400)
    
    def initialize(direction):
        self.ser.write(b"IZ", direction.encode(), b"\r")
        
        
