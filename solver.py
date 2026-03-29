from board import Board
from marble import Marble
from rules import get_match
class Solver:
    def __init__(self,board=None):
        self.board=board
        self.moves=[]

    def set_board(self,board):
        self.board=board

    def solve_board(self):
        self.is_enabled(5)
        pass

    def is_enabled(self,index):
        marble=self.board.get_marble(index).type
        if marble==None:
            return False
        

    def get_row_length(self,row):
        if row==0:
            return 6
        if row==1:
            return 7
        if row==2:
            return 8
        if row==3:
            return 9
        if row==4:
            return 10
        if row==5:
            return 11
        if row==6:
            return 10
        if row==7:
            return 9
        if row==8:
            return 8
        if row==9:
            return 7
        if row==10:
            return 6
        
        

    def index_to_row(self,index):
        if index<6:
            return 0
        if index<13:
            return 1
        if index<21:
            return 2
        if index<30:
            return 3
        if index<40:
            return 4
        if index<51:
            return 5
        if index<61:
            return 6
        if index<70:
            return 7
        if index<78:
            return 8
        if index<85:
            return 9
        return 10
        
        
        