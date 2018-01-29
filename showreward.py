def showReward(reward):
    if ( reward < -5 ):
        return "VERY LOW"
    elif ( reward >= -5 and reward < 0 ):
        return "LOW"
    elif ( reward == 0 ):
        return "MEDIUM"
    elif ( reward > 0 and reward < 10 ):
        return "HIGH"
    elif ( reward >= 10 ):
        return "VERY HIGH"   
def showLocation( x,y ):
    return "%d %d" % (x, y)
def showThoughts( n, s, e, w):
    if ( n - s - w - e == 0):
        return "GUESS"
    elif ( n > 0 ):
        return "UP"
    elif ( s > 0):
        return "DOWN"
    elif ( e > 0):
        return "RIGHT"
    else:
        return "LEFT"
    
    
        
    
