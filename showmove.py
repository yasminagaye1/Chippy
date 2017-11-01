import os
import QueueTest
a = 0
q = QueueTest.Queue()
def showmove(direction, reward):
        global a
        global q
        q.enqueue(direction)
        q.enqueue(reward)
        directions = open ("commands.txt","a")
        directions.write ("%s %s \n" % (str(direction) , str(reward) ) )
        directions.close()
        print ( q.size() )


def clear():
        global q
        q = QueueTest.Queue()
        directions = open ( "commands.txt" , "w" )
        directions.close()
        print ( "queue has been cleared")
