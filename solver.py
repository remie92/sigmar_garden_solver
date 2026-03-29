from board import Board
from marble import Marble
from rules import Rules
class Solver:
    def __init__(self,board=None):
        self.board=board
        self.moves=[]

    def set_board(self,board):
        self.board=board

    def solve_board(self):
        pass