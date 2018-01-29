import os
import QueueTest
a = 0
q = QueueTest.Queue()
def showmove(direction, reward):
        global a
        global q
        q.enqueue(direction)
        q.enqueue(reward)
        directions = open ("/Users/chrisbanks/Desktop/WORKFILES/chippy/direct/commands.txt","a")
        directions.write ("%s %s \n" % (str(direction) , str(reward) ) )
        directions.close()
        print ( q.size() )


def clear():
        global q
        q = QueueTest.Queue()
        directions = open ( "/Users/chrisbanks/Desktop/WORKFILES/chippy/direct/commands.txt" , "w" )
        directions.close()
        print ( "queue has been cleared")





        
#        if ( direction == 0):
#            directions = open("/Users/chrisbanks/Desktop/WORKFILES/chippy/direct/%s.txt" % str(a), "w+")
#            directions.write( "0" )
#            directions.close()
#            os.remove("/Users/chrisbanks/Desktop/WORKFILES/chippy/direct/%s.txt" % str(a))
#        elif ( direction == 1 ):
#            directions = open("/Users/chrisbanks/Desktop/WORKFILES/chippy/direct/%s.txt" % str(a), "w+")
#            directions.write("1")
#            directions.close()
#            os.remove("/Users/chrisbanks/Desktop/WORKFILES/chippy/direct/%s.txt" % str(a))
#        elif ( direction == 2):
#            directions = open("/Users/chrisbanks/Desktop/WORKFILES/chippy/direct/%s.txt" % str(a), "w+")
#            directions.write("2")
#            directions.close()
#            os.remove("/Users/chrisbanks/Desktop/WORKFILES/chippy/direct/%s.txt" % str(a))
#        elif ( direction == 3):
#            directions = open("/Users/chrisbanks/Desktop/WORKFILES/chippy/direct/%s.txt" % str(a), "w+")
#            directions.write("3")
#            directions.close()
#            os.remove("/Users/chrisbanks/Desktop/WORKFILES/chippy/direct/%s.txt" % str(a))
#        a += 1
#        print (direction)
