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
        