from  marble import Marble

class Board:
    def __init__(self):
        self.board=[]
        for i in range(0,91):
            self.board.append(Marble())

    def set_type(self,type,index):
        if(type=="empty"):
            self.board[index].set_type(None)
        else:
            self.board[index].set_type(type)

    def get_marble(self,index):
        return self.board[index]

    def __str__(self):
        output=""
        counter=0
        for i in range(0, 11):
            i_center_dist = abs(5 - i)
            row_size = 11 - i_center_dist
            line=""
            for j in range(0, row_size):
                line+=f"[{i}.{j}.{self.board[counter].type}]"
                counter+=1
            line+="\n"
            output+=line
        return output
