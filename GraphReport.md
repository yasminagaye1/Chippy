
</b>GRAPHS FOR EACH LEVEL OF CHIPPY</b>

The goal of this project so far was to gain an insight on how Chippy 
works internally. To do so, we modified the Constants.py file to reduce the number 
of experiments and number of rewards from 22 to 1 and from 7 to 2 respectively.

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


We can see that Chippy tends to behave more closely to intuition as we
go from level0 to level 4. At level 4, chippy continues to garner rewards
until expected result and actual results do not match up then it has to 
either learn or reset.



******
NOTES
******

*Rewards location are always at points (0,0) and (7,7) 
    in the 8X8 square matrix
*Each square in the matrix has an expected and actual reward
*Each experiment switches between two rewards
*A switch between two reward values is the change
    in seasonality we are looking for
*If youve seen a switch between two reward (or a season)
    change then check the qtable to see if youve
    seen that pattern before else add it to the qtable
*If that season change already exists in the qtable then use 
    the same trajectory as before that was learned using the 
    reinforcement learner to get to the rewards
*So anytime you learn a movement through a new pattern (season)
    save your path somewhere in the qtable
*this table will be a dictionary structure with the 
    reward(value or location??) as the key and the path as the value
*If chippy knows the path to get to a location, it can just go 
    straight without beating around the bush to find 'best direction'
*This code does not have backtracking or recursion so how 
    do retrace our steps when we make a bad move? find best move
*Where does kasai fit into this?