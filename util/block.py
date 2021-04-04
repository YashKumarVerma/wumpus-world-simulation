# class to realize a block in the program
class Block:
    NOT_PRESENT = 0
    UNSURE = 1
    
    hasBreeze = False
    hasPit = False
    pitStatus = UNSURE
    
    hasStench = False
    hasWumpus = False
    wumpusStatus = False
    
    hasGold = False
    isVisited = False
