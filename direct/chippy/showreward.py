def showReward(reward):
    if ( reward < -5 ):
        return "VERY LOW"
    elif ( reward >= -5 and reward < 0 ):
        return "LOW"
    elif ( reward >= 0 and reward < 5):
        return "MEDIUM"
    elif ( reward >= 5 and reward < 10 ):
        return "HIGH"
    elif ( reward >= 10 ):
        return "VERY HIGH"
    
def showLocation( x,y ):
    return "%d %d" % (x, y)


        
    
