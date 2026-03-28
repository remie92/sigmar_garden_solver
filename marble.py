class Marble:
    def __init__(self,type=None):
        self.type=type
    
    def __str__(self):
        return f"Marble Type: {type}"