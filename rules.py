rules={
    "salt":["salt","water","air","earth","fire"],
    "fire":["fire","salt"],
    "water":["water","salt"],
    "air":["air","salt"],
    "earth":["earth","salt"],
    "mors":["vitae"],
    "vitae":["mors"]
}

def is_valid(type1,type2,metal_order):
    if rules.get(type1)!=None:
        if type2 in  rules.get(type1):  #STATIC RULES
            return True
        else:
            return False
        
    if type2=="quicksilver":
        type2=type1
        type1="quicksilver"

    if type1=="quicksilver":
        if metal_order==0 and type2=="lead":
            return True
        elif metal_order==1 and type2=="tin":
            return True
        elif metal_order==2 and type2=="iron":
            return True
        elif metal_order==3 and type2=="copper":
            return True
        elif metal_order==4 and type2=="silver":
            return True
        elif metal_order==5 and type2=="gold":
            return True




print(is_valid("quicksilver","lead",0))