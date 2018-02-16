
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


NOTES
*****
*Runners inherits runner which inherits qlearner, which inherits walker

*Still dont know when and how monitor is called but thats btw

*The learner should have mastered its grid and rewards just b4 we switch
    so save the grid and its qvalues just b4 the end of  10000 moves

*And b4 we start any moves in any experiment, check if the rewards in 
    the particular setting has been seen before. If the pattern has been
    seen b4 then program chippy to follow the qtable in its movement


NOTES
*****
*The move() in experiment.py calls the move() in runner.py,
    which calls the move() in qlearner.py, which calls the 
    suggest() in walker, which calls suggest in grid

*monitor() in runner.py calls monitor() in runners.py that 
    monitors the results and gives a suggestion. This activity
    is implmented using inheritance so a quick glance at python's
    use of inheritance could aid grasping of the concepts.

*Now that we know how everything works... We need to record the best
    qtable of an experiment. So when the number of steps is close 
    to 10000, we save all the table values as values in a dictionary 
    structure and use the experiment rewards as keys.

*Implement a new suggest called SUGGEST_MAINTAIN that checks if
    the current experiment pattern has already been seen before.
    If yes then load the qtable from the qtable dictionary. 

*To save the particular qtable pass a variable that will notify 
    square when it is time to save the current table. All squares 
    have qvalues and these values should be fed into directions, 
    and policy. 

NOTES
*****
*I have figured out a way to return q values from the graph to experiments
    or wherever I need them

*Modifying runners.py by looking at kenneth's code to figure how to manipulate
    make chippy check if it has seen a pattern before and to use 
    particular q values.

*Still thinking of how to force chippy to use a certain qvalue even 
    after knowing that it has seen a particular experiment before

NOTES
******
*I have found a way to send rewards and qvalues (archQdic) from 
    experiment.py to runners.py, which contains the monitor()
*Montor() will check if the actual rewards is less than the expected
    reward. 
*Our class model will then check the archQdic to see if we have 
    seen the pattern before. If so then figure out how to make 
    chippy use the qvalues from archQdic