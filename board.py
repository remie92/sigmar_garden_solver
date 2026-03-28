from  marble import Marble

class Board:
    def __init__(self):
        board=[]
        for i in range(0,91):
            board.append(Marble())