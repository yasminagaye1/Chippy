
GRAPHS FOR EACH LEVEL OF CHIPPY

The goal of this project so far was to gain an insight of how Chippy 
works internally. To do so, we modified the Constants.py file to reduce the number 
of experiments and number of rewards from 22 to 1 and from 7 to 2.

The experiment (EXPERIMENTS=[(0,1)]) will switch between two reward tuples ([(-100, 10), (100,  -50)])
over a total of 20,000 steps in 20 repeats. Therefore the total numnber of steps 
for each experiment is exactly 400,000.

Chippy also has cognitive levels. listed in the runners.py classes.
CLASSES = {
    LEVEL0HC:   Level0,
    LEVEL1HCA:  Level1HCA,
    LEVEL1HCB:  Level1HCB,
    LEVEL2HC:   Level2HC,
    LEVEL3HC:   Level3HC,
    LEVEL2MCL:  MCL2,
    LEVEL3MCL:  MCL3
}

The logical operations for each class can be found in runners.py. 
From observations and experimentation, it is clear that LEVEL3HC above
carries out more cognitive funtinality than any other level in the class.
This distinction is evident in its more patterned graph. 

LEVEL3HC throws away its current Qtable when expected result is 
greater than actual result and begins to learn. 


We ran ./Dissertation.py using the setting described above for 
CLASS 0-4 since 5 and 6 are mere repititions of class 1.


./Dissertation.py -l 0
![alt text](https://github.com/tabularrasa/Chippy/blob/JesuyeChippy/allPix/graphlevel0.PNG)


./Dissertation.py -l 1
![alt text](https://github.com/tabularrasa/Chippy/blob/JesuyeChippy/allPix/graphlevel1.PNG)

./Dissertation.py -l 2
![alt text](https://github.com/tabularrasa/Chippy/blob/JesuyeChippy/allPix/graphlevel2.PNG)


./Dissertation.py -l 3
![alt text](https://github.com/tabularrasa/Chippy/blob/JesuyeChippy/allPix/graphlevel3.PNG)


./Dissertation.py -l 4
![alt text](https://github.com/tabularrasa/Chippy/blob/JesuyeChippy/allPix/graphlevel4.PNG)


