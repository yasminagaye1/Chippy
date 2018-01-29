import os
import QueueTest
a = 0
q = QueueTest.Queue()
def showmove(location, reward):
        global a
        global q
        q.enqueue(location)
        q.enqueue(reward)
        directions = open ("commands.txt","a")
        directions.write ("%s %s \n" % (str(location) , str(reward) ) )
        directions.close()
        print ( q.size() )
def showThoughts(inference):
        directions = open("commands.txt", "a")
        directions.write("%s\n" % inference)
        directions.close()
        print (inference)

def clear():
        global q
        q = QueueTest.Queue()
        directions = open ( "commands.txt" , "w" )
        directions.close()
        print ( "queue has been cleared")
