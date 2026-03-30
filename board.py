from  marble import Marble
from rules import get_match
class Board:
    def __init__(self):
        self.board=[]
        self.metal_order=0
        self.moves=[]
        for i in range(0,91):
            self.board.append(Marble())

    def set_type(self,type,index):
        if(type=="empty"):
            self.board[index].set_type(None)
        else:
            self.board[index].set_type(type)

    def get_marble(self,index):
        return self.board[index]
    
    
    def copy(self):
        new_board = Board()
        for i in range(91):
            new_board.board[i].set_type(self.board[i].type)
        new_board.metal_order = self.metal_order
        new_board.moves = self.moves[:]  # shallow copy of the list
        return new_board
        

    def get_all_permutations(self):
        enabled_indexes=[]
        for i in  range(91):
            if self.is_enabled(i):
                enabled_indexes.append(i)
        new_boards=[]
        if self.metal_order==5 and self.is_enabled(45):
            new_board=self.copy()
            new_board.moves.append((45))
            new_board.board[45]=Marble()
            new_boards.append(new_board)
        for i in range(len(enabled_indexes)):
            index1=enabled_indexes[i]
            for j in range(len(enabled_indexes)):
                if  i!=j:
                    index2=enabled_indexes[j]
                    match_type=get_match(self.board[index1].type,self.board[index2].type,self.metal_order)
                    if match_type:
                        new_board=self.copy()
                        if match_type==2:
                            new_board.metal_order+=1
                        new_board.moves.append((index1,index2))
                        new_board.board[index1]=Marble()
                        new_board.board[index2]=Marble()
                        new_boards.append(new_board)
            
        return  new_boards
    
    def generate_id_num(self):
        id_num=0
        for i in  range(91):
            id=self.board[i].type
            if id==None:
                id=14
            id_num+=pow(15,i)*id

        return id_num

    
    def count_marbles(self):
        count=0
        for i in  range(91):
            if self.board[i].type!=None:
                count+=1
        return count
    
    def count_enabled_marbles(self):
        count=0
        for i in range(91):
            if self.is_enabled(i):
                count+=1
        return count
    

    def won_game(self):
        for i in  range(91):
            if self.board[i].type!=None:
                return False
        return True
                
        
    

    def is_enabled(self,index):
        marble=self.get_marble(index).type
        if marble==None:
            return False
        
        marble_l=self.get_left_marble(index).type==None
        marble_r=self.get_right_marble(index).type==None
        marble_tl=self.get_top_left_marble(index).type==None
        marble_tr=self.get_top_right_marble(index).type==None
        marble_bl=self.get_bottom_left_marble(index).type==None
        marble_br=self.get_bottom_right_marble(index).type==None
        if marble_l and marble_tl and marble_tr:
            return True
        if marble_tl and marble_tr and marble_r:
            return True
        if marble_tr and marble_r and marble_br:
            return True
        if marble_r and marble_br and marble_bl:
            return True
        if marble_br and marble_bl and marble_l:
            return True
        if marble_bl and marble_l and marble_tl:
            return True
        return False
    

    def get_left_marble(self,index):
        if index in [0,6,13,21,30,40,51,61,70,78,85]:
            return Marble()
        else:
            return self.get_marble(index-1)
        
    def get_top_left_marble(self,index):
        row=self.index_to_row(index)
        if row==0 or index in [0,6,13,21,30,40]:
            return Marble()
        else:
            prev_length=self.get_row_length(row-1)
            max_length=max(prev_length,self.get_row_length(row))
            return self.get_marble(index-max_length)
        
    def get_top_right_marble(self,index):
        row=self.index_to_row(index)
        if row==0 or index in [5,12,20,29,39,50]:
            return Marble()
        else:
            prev_length=self.get_row_length(row-1)
            max_length=max(prev_length,self.get_row_length(row))
            return self.get_marble(index-max_length+1)
        
    def get_bottom_left_marble(self,index):
        row=self.index_to_row(index)
        if row==10 or index in [40,51,61,70,78,85]:
            return Marble()
        else:
            prev_length=self.get_row_length(row+1)
            max_length=max(prev_length,self.get_row_length(row))
            return self.get_marble(index+max_length-1)
        
    def get_bottom_right_marble(self,index):
        row=self.index_to_row(index)
        if row==10 or index in [50,60,69,77,84,90]:
            return Marble()
        else:
            prev_length=self.get_row_length(row+1)
            max_length=max(prev_length,self.get_row_length(row))
            return self.get_marble(index+max_length)
        
    def get_right_marble(self,index):
        if index in [5,12,20,29,39,50,60,69,77,84,90]:
            return Marble()
        else:
            return self.get_marble(index+1)
        

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
