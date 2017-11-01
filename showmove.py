def showmove(direction):
        a = 0
        if ( direction == 0):
            directions = open("%s.txt" % str.a, "r+")
            ++a
            directions.write( "0" )
            directions.close()
            pygame.time.wait(delay+1000)
        elif ( direction == 1 ):
            directions = open("%s.txt" % str.a, "r+")
            ++a
            directions.write("1")
            directions.close()
            pygame.time.wait(delay)
        elif ( direction == 2):
            directions = open("%s.txt" % str.a, "r+")
            ++a
            directions.write("2")
            directions.close()
            pygame.time.wait(delay)
        elif ( direction == 3):
            directions = open("%s.txt" % str.a, "r+")
            ++a
            directions.write("3")
            directions.close()
            pygame.time.wait(delay)
        
        print (direction)
