import os
import re
p = re.compile('[0-9]+.txt')
root = "/Users/chrisbanks"
for file in os.walk(root):
        if file == p.match:
            os.remove(filename)
        
