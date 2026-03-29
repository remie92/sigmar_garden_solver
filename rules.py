type_to_index={
    "salt":0,
    "air":1,
    "fire":2,
    "water":3,
    "earth":4,
    "vitae":5,
    "mors":6,
    "quicksilver":7,
    "lead":8,
    "tin":9,
    "iron":10,
    "copper":11,
    "silver":12,
    "gold":13,
    
}



rules={
    0:[0,3,1,4,2],
    2:[2,0],
    3:[3,0],
    1:[1,0],
    4:[4,0],
    6:[5],
    5:[6]
}

def get_match(type1,type2,metal_order):
    if rules.get(type1)!=None:
        if type2 in  rules.get(type1):  #STATIC RULES
            return 1
        else:
            return 0
        
    if type2==7:
        type2=type1
        type1=7

    if type1==7:
        if metal_order==0 and type2==8:
            return 2
        elif metal_order==1 and type2==9:
            return 2
        elif metal_order==2 and type2==10:
            return 2
        elif metal_order==3 and type2==11:
            return 2
        elif metal_order==4 and type2==12:
            return 2
        elif metal_order==5 and type2==13:
            return 2
        else:
            return 0
    return 0

