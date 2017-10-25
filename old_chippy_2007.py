# ====================================================================
#                            c h i p p y . p y
# ====================================================================

# Author:  Dean Earl Wright III
# Created: 19 April 2007
# Purpose: Reimplementation of the Q-learning perturbation testbed
#          use for the initial Meta-cognitive Loop testing.

# --------------------------------------------------------------------
#                                                              imports
# --------------------------------------------------------------------
import math, unittest, random, csv

# --------------------------------------------------------------------
#                                                            constants
# --------------------------------------------------------------------
DIR_N = 0
DIR_S = 1
DIR_E = 2
DIR_W = 3
DIR_DELTA_X = [ 0,  0,  1, -1]
DIR_DELTA_Y = [-1,  1,  0,  0]

# ====================================================================
#                                                               Square
# ====================================================================
class Square(object):
    "A single square of a grid world."
    def __init__(self, reward=0, x=0, y=0, jump=None):
        self.__reward  = reward
        self.__x       = x
        self.__y       = y
        self.__jump    = jump
        self.__q       = [0.0,0.0,0.0,0.0]

    def __str__(self):
        return "[%d,%d] r=%d" % (self.__x, self.__y, self.__reward)

    def reward(self):  return self.__reward
    def x(self):       return self.__x
    def y(self):       return self.__y
    def loc(self):     return (self.__x, self.__y)
    def jump(self):    return self.__jump
    def q(self):       return self.__q

    def set_reward(self, reward):
        self.__reward = reward

    def set_jump(self, jump):
        self.__jump = jump
        
    def __setitem__(self, index, value):
        self.__q[index] = value    
        
    def __getitem__(self, index):
        return self.__q[index]
        
    def reset(self):
        self.__q = [0.0,0.0,0.0,0.0]
        
    def suggest(self):
        "Suggest the highest ranked move"
        
        # 1. Start by picking a random direction
        pick = random.randint(0,3)
        result = [pick]
        value  = self.__q[pick]
        
        # 2. Loop for the other directions
        for dir in range(4):
            if dir == pick: continue
            
            # 3. If this direction is better, save it
            v = self.__q[dir]
            if v > value:
                value = v
                result = [dir]
                
            # 4. If the same, keep both (or more)    
            elif v == value:
                result.append(dir)
                
        # 5. If there is more than one best direction, shuffle them
        if len(result) > 1:
            random.shuffle(result) 
            
        # 6. Return the best direction (or directions)         
        return result
        
    def max(self):   
        value  = self.__q[0]
        for dir in [1,2,3]:
            v = self.__q[dir]
            if v > value:
                value = v
        return value
        
# ====================================================================
#                                                                 Grid
# ====================================================================
class Grid(object):
    "Multiple squares arranged in an n by n matrix with two rewards"
    
    def __init__(self, n=8, r1=10, r2=-10):
        "Initialize a n-armed bandit"
        
        # 1. Set local values
        self.__n_1     = n-1
        self.__squares = {}
        self.__r1      = r1
        self.__r2      = r2 
        
        # 2. Create all the individual squares
        for x in range(n):
            for y in range(n):
                s = Square(x=x, y=y)
                self.__squares[(x,y)] = s
        
        # 3. Set the rewards
        self.set_rewards(r1,r2)

        # 4. Set the transporters
        self.__squares[(0,0)].set_jump((self.__n_1,self.__n_1))
        self.__squares[(self.__n_1,self.__n_1)].set_jump((0,0))

    def __str__(self):
        return "Grid (n=%d,r1=%d,r2=%d)" % \
               (self.__n_1+1, self.__r1, self.__r2)

    def n(self):       return self.__n_1+1
    def r1(self):      return self.__r1
    def r2(self):      return self.__r2
    def rewards(self): return (self.__r1, self.__r2)

    def set_rewards(self, r1=0, r2=0):
        self.__r1      = r1
        self.__r2      = r2 
        self.__squares[(0,0)].set_reward(r1)
        self.__squares[(self.__n_1,self.__n_1)].set_reward(r2)

    def __getitem__(self, index):
        return self.__squares[index]

    def __len__(self):
        return len(self.__squares)

    def move(self, at, dir):
        "From square 'at' move in direction 'dir'"
    
        # 1. Determine new square
        new_x = at[0] + DIR_DELTA_X[dir]
        if new_x < 0:          new_x = 0
        if new_x > self.__n_1: new_x = self.__n_1
        new_y = at[1] + DIR_DELTA_Y[dir]
        if new_y < 0:          new_y = 0
        if new_y > self.__n_1: new_y = self.__n_1
        new_xy = (new_x, new_y)
        
        # 2. No reward or jumps if new position is same as old
        if at == new_xy: return (0, at)
        
        # 3. Get reward for moving to the new square
        reward = self.__squares[new_xy].reward()
        
        # 4. Implement jumps at reward squares
        jump = self.__squares[new_xy].jump()
        if None != jump: new_xy = jump
        
        # 5. Return reward and new location
        return (reward, new_xy)

    def reset(self):
        for s in self.__squares:
            s.reset()    
            
    def suggest(self, loc):
        return self.__squares[loc].suggest()

    def switch(self):
        "Switch the values of the two rewards"
        old_r1 = self.__r1
        old_r2 = self.__r2
        self.set_rewards(old_r2, old_r1)
                        
# ====================================================================
#                                                               Walker
# ====================================================================
class Walker(object):
    "A grid crawling agent"
    
    def __init__(self, grid=None, start=None):
        self.__score   = 0
        self.__count   = 0
        self.__grid    = grid
        if grid == None:
            if start == None:
                self.__loc = (0,0)
            else:
                self.__log = start
        else:             
            if start == None:
                self.__loc = (grid.n()/2, grid.n()/2)
            else:    
                self.__loc = start 

    def __str__(self):
        return "Walker (c=%d,s=%d,l=%s %s)" % \
               (self.__count, self.__score, 
                str(self.__loc), str(self.__grid))

    def score(self):   return self.__score
    def count(self):   return self.__count
    def grid(self):    return self.__grid
    def loc(self):     return self.__loc
    
    def move(self, dir=None):
        "Move to the given, best, or random direction"
        
        # 1. Pick a direction if none given
        if None == dir: 
            suggest = self.suggest()
            dir = suggest[random.randint(0, len(suggest))]
        
        # 2. Move and get reward and new location
        (reward, loc) = self.__grid.move(self.__loc, dir)
        
        # 3. Set new location
        self.__loc = loc
        
        # 4. Accumulate the reward
        self.__score = self.__score + reward
        
        # 5. Count the number of moves
        self.__count = self.__count + 1
        
        # 6. Return reward and new location
        return (reward, loc)

    def suggest(self):
        return self.__grid.suggest(self.__loc)
        
# ====================================================================
#                                                             QLearner
# ====================================================================
class QLearner(Walker):
    def __init__(self, grid=None, start=None,
                  alpha=0.5, gamma=0.9, epsilon=0.05):
        Walker.__init__(self, grid=grid, start=start)
        self.__alpha   = alpha
        self.__gamma   = gamma
        self.__epsilon = epsilon

    def __str__(self):
        return "QLearner (a=%f,g=%f,e=%f,c=%d,s=%f %s)" % \
               (self.__alpha,self.__gamma,self.__epsilon, self.count(),
                self.score(), str(self.grid()))

    def epsilon(self): return self.__epsilon
    def alpha(self): return self.__alpha
    def gamma(self): return self.__gamma

    def set_epsilon(self, epsilon): self.__epsilon = epsilon
    def set_alpha(self, alpha): self.__alpha = alpha
    def set_gamma(self, gamma): self.__gamma = gamma

    def move(self, dir=None):
        "Move in the direction with the best expected value or explore"
    
        # 1. Remember the previous location
        previous = self.loc()
    
        # 2. Get suggested direction
        if dir == None:
            dir = Walker.suggest(self)[0]
        
            # 3. If exploring, get a random direction
            if self.__epsilon > random.random():
                dir = random.randint(0,3)
            
        # 4. Move in specified direction     
        result = Walker.move(self, dir=dir)
        
        # 5. Adjust the action expected rewards
        self.qreward(dir, previous, result[0], result[1])
            
        # 6. Return reward and new location
        return result
        
    def qreward(self, a, s, r, sp):
        "Spread out the reward over the past moves"
        oldQsa = self.grid()[s][a]
        maxQspap = self.grid()[sp].max()
        newQsa = oldQsa + self.__alpha*(r + (self.__gamma*maxQspap) - oldQsa)
        print "Q([%d,%d],%d) = %f = %f + %f(%f + %f(%f-%f))" % \
            (s[0], s[1], a, newQsa, oldQsa, 
             self.__alpha, r, self.__gamma, maxQspap, oldQsa)
        self.grid()[s][a] = newQsa
        return newQsa
        
        
# ====================================================================
#                                                       RollingAverage
# ====================================================================
class RollingAverage(object):
    def __init__(self, n=200):
        self.__values = []
        self.__n      = n
        self.__total  = 0.0
        
    def add(self, number):
        if len(self.__values) == self.__n:
            self.__total = self.__total - self.__values[0]
            self.__values = self.__values[1:]
            
        self.__values.append(number)
        self.__total = self.__total + number
        
    def __len__(self): return len(self.__values)
    def count(self):   return len(self.__values)
    def n(self):       return self.__n
    def total(self):   return self.__total
    def average(self):
        if 0 == len(self.__values):
            return 0.0
        else:     
            return self.__total / float(len(self.__values))

# ====================================================================
#                                                               vector
# ====================================================================
class Vector(object):
    def __init__(self, data):
        self.__vec = data
    
    def __repr__(self):
        return repr(self.__vec)  
    
    def __add__(self, other):
        return Vector(map(lambda x, y: x+y, self, other))

    def __div__(self, other):
        return Vector(map(lambda x, y: x/y, self, other))

    def __getitem__(self, index):
        return self.__vec[index]

    def __len__(self):
        return len(self.__vec)

# ====================================================================
#                                                                stats
# ====================================================================
class Stats(object):
    def __init__(self):
        self.__data = {}
        self.__knts = {}

    def __getitem__(self, key): return self.__data[key]
    
    def add(self, key, data):
        if key in self.__data:
            self.__data[key] = self.__data[key] + data
            self.__knts[key] = self.__knts[key] + 1
        else:
            self.__data[key] = Vector(data)    
            self.__knts[key] = 1
            
    def average(self, key):
        return self.__data[key] / Vector(len(self.__data[key])*(float(self.__knts[key]),))
        
        
# ====================================================================
#                                                          experiments
# ====================================================================
def experiments(repeat=20, steps=20000):
    "Do the chippy experiment"

    # 1. Create the statistics object that will collect the data
    stats = Stats()
    
    # 2. Repeat several times to smooth the curves
    for num in xrange(repeat):
        print num, 
        
        # 3. Run the experiment without perterbation
        result = experiment(steps=steps+200)
        
        # 4. Record the results
        stats.add("normal", result)
        
        # 5. Run the experiment with perterbation
        result = experiment(steps=steps, switch=steps/2)
        
        # 6. Record the results
        stats.add("switch", result)
        
        # 7. Run the experiment with perterbation and mcl
        #result = experiment(steps=steps, switch=steps/2)
        
        # 8. Record the results
        stats.add("mcl", result)
        
    print "OK"        
    
    # 9. Get the averages
    normal = stats.average("normal")
    switch = stats.average("switch")
    mcl    = stats.average("mcl")
    
    # 10. Write the averages in a comma seperated values file
    f = open("chippy.csv", "w")
    f.write("step,normal,switch,mcl\n")
    for step in xrange(steps-200):
        f.write("%d,%f,%f,%f\n" % \
                (step, normal[step+200], switch[step+200], mcl[step+200]))
    f.close()
    
# ====================================================================
#                                                           experiment
# ====================================================================
def experiment(steps=20000, switch=-1):
    "Do the chippy experiment"

    # 1. Create the objects
    grid = Grid(r1=10,r2=-10)
    qlrn = QLearner(grid=grid)
    ravg = RollingAverage()
    
    # 2. Start with no results
    results = []
    
    # 3. Walk a mile in chippy's shoes
    for step in xrange(steps):
        reward = qlrn.move()[0]

        # 4. Record this reward in the averages
        ravg.add(reward)
        
        # 5. Record the average in the results
        results.append(ravg.average())
        
        # 6. Switch the rewards if it is time
        if step == switch: 
            grid.switch()
        
    # 7. Return the rolling averages
    return results
        
# ====================================================================
#                                                           unit tests
# ====================================================================
class TestSquare(unittest.TestCase):

    def testEmptyConstructor(self):
        s = Square()
        self.assertEqual(s.reward(),        0)
        self.assertEqual(s.x(),             0)
        self.assertEqual(s.y(),             0)
        self.assertEqual(s.loc(),       (0,0))
        self.assertEqual(str(s),  "[0,0] r=0")
        self.assertEqual(s.jump(),       None)
        s.set_reward(10)
        self.assertEqual(s.reward(),       10)
        self.assertEqual(s.x(),             0)
        self.assertEqual(s.y(),             0)
        self.assertEqual(s.loc(),       (0,0))
        self.assertEqual(str(s), "[0,0] r=10")
        self.assertEqual(s.jump(),       None)
        s.set_jump((3,3))
        self.assertEqual(s.reward(),       10)
        self.assertEqual(s.x(),             0)
        self.assertEqual(s.y(),             0)
        self.assertEqual(s.loc(),       (0,0))
        self.assertEqual(str(s), "[0,0] r=10")
        self.assertEqual(s.jump(),      (3,3))

    def testConstructor(self):
        s = Square(reward=10, x=4, y=3)
        self.assertEqual(s.reward(),        10)
        self.assertEqual(s.x(),              4)
        self.assertEqual(s.y(),              3)
        self.assertEqual(s.loc(),        (4,3))
        self.assertEqual(str(s),  "[4,3] r=10")
        self.assertEqual(s.jump(),       None)
        s.set_reward(6)
        self.assertEqual(s.reward(),         6)
        self.assertEqual(s.x(),              4)
        self.assertEqual(s.y(),              3)
        self.assertEqual(s.loc(),        (4,3))
        self.assertEqual(str(s),   "[4,3] r=6")
        self.assertEqual(s.jump(),       None)

    def testSuggestions(self):
        s = Square(reward=10, x=4, y=3)
        self.assertEqual(len(s.suggest()), 4)
        s[0] = 3.4
        self.assertEqual(s.suggest(), [0])
        s[2] = 4.3
        self.assertEqual(s.suggest(), [2])
        s[1] = 1.2
        self.assertEqual(s.suggest(), [2])
        s[3] = 1.2
        self.assertEqual(s.suggest(), [2])
        s[1] = 4.3
        sug = s.suggest()
        self.assert_(sug == [1,2] or sug == [2,1]) 

class TestGrid(unittest.TestCase):

    def testEmptyConstructor(self):
        g = Grid()
        self.assertEqual(g.n(),              8)
        self.assertEqual(g.r1(),            10)
        self.assertEqual(g.r2(),           -10)
        self.assertEqual(g.rewards(), (10,-10))
        self.assertEqual(len(g),            64)
        self.assertEqual(str(g),   "Grid (n=8,r1=10,r2=-10)")
        g.set_rewards()
        self.assertEqual(g.n(),              8)
        self.assertEqual(g.r1(),             0)
        self.assertEqual(g.r2(),             0)
        self.assertEqual(g.rewards(),    (0,0))
        self.assertEqual(len(g),            64)
        self.assertEqual(str(g),   "Grid (n=8,r1=0,r2=0)")

    def testConstructor(self):
        g = Grid(n=6, r1=4, r2=3)
        self.assertEqual(g.n(),              6)
        self.assertEqual(g.r1(),             4)
        self.assertEqual(g.r2(),             3)
        self.assertEqual(g.rewards(),    (4,3))
        self.assertEqual(len(g),            36)
        self.assertEqual(str(g),   "Grid (n=6,r1=4,r2=3)")
        g.set_rewards(r1=2, r2=6)
        self.assertEqual(g.n(),              6)
        self.assertEqual(g.r1(),             2)
        self.assertEqual(g.r2(),             6)
        self.assertEqual(g.rewards(),    (2,6))
        self.assertEqual(len(g),             36)
        self.assertEqual(str(g),   "Grid (n=6,r1=2,r2=6)")

    def testMoves(self):
        g = Grid(r1=1,r2=2)
        self.assertEqual(g.n(),              8)
        self.assertEqual(g.r1(),             1)
        self.assertEqual(g.r2(),             2)
        self.assertEqual(g.move((3,3),0), (0,(3,2)))    
        self.assertEqual(g.move((3,3),1), (0,(3,4)))    
        self.assertEqual(g.move((3,3),2), (0,(4,3)))    
        self.assertEqual(g.move((3,3),3), (0,(2,3)))    
        self.assertEqual(g.move((3,7),0), (0,(3,6)))    
        self.assertEqual(g.move((3,7),1), (0,(3,7)))    
        self.assertEqual(g.move((3,7),2), (0,(4,7)))    
        self.assertEqual(g.move((3,7),3), (0,(2,7)))    
        self.assertEqual(g.move((3,0),0), (0,(3,0)))    
        self.assertEqual(g.move((3,0),1), (0,(3,1)))    
        self.assertEqual(g.move((3,0),2), (0,(4,0)))    
        self.assertEqual(g.move((3,0),3), (0,(2,0)))    
        self.assertEqual(g.move((7,3),0), (0,(7,2)))    
        self.assertEqual(g.move((7,3),1), (0,(7,4)))    
        self.assertEqual(g.move((7,3),2), (0,(7,3)))    
        self.assertEqual(g.move((7,3),3), (0,(6,3)))    
        self.assertEqual(g.move((0,3),0), (0,(0,2)))    
        self.assertEqual(g.move((0,3),1), (0,(0,4)))    
        self.assertEqual(g.move((0,3),2), (0,(1,3)))    
        self.assertEqual(g.move((0,3),3), (0,(0,3)))    
        self.assertEqual(g.move((0,1),0), (1,(7,7)))    
        self.assertEqual(g.move((1,0),3), (1,(7,7)))    
        self.assertEqual(g.move((6,7),2), (2,(0,0)))    
        self.assertEqual(g.move((7,6),1), (2,(0,0)))    
        self.assertEqual(g.move((0,0),0), (0,(0,0)))    
        self.assertEqual(g.move((0,0),DIR_N), (0,(0,0)))    

    def testSquares(self):
        g = Grid(r1=1,r2=2)
        self.assertEqual(g.n(),              8)
        self.assertEqual(g.r1(),             1)
        self.assertEqual(g.r2(),             2)
        self.assertEqual(g[(0,0)].reward(),  1)
        self.assertEqual(g[(7,7)].reward(),  2)
        self.assertEqual(g[(3,4)].x(),       3)
        self.assertEqual(g[(3,5)].y(),       5)
        self.assertEqual(g[(6,7)].loc(), (6,7))
        g.switch()
        self.assertEqual(g.n(),              8)
        self.assertEqual(g.r1(),             2)
        self.assertEqual(g.r2(),             1)
        self.assertEqual(g[(0,0)].reward(),  2)
        self.assertEqual(g[(7,7)].reward(),  1)

class TestWalker(unittest.TestCase):

    def testEmptyConstructor(self):
        w = Walker()
        self.assertEqual(w.score(),          0)
        self.assertEqual(w.count(),          0)
        self.assertEqual(w.loc(),        (0,0))
        self.assertEqual(str(w),  "Walker (c=0,s=0,l=(0, 0) None)")

    def testConstructor(self):
        g = Grid()
        w = Walker(grid=g)
        self.assertEqual(w.score(),          0)
        self.assertEqual(w.count(),          0)
        self.assertEqual(w.loc(),        (4,4))
        self.assertEqual(str(w),  "Walker (c=0,s=0,l=(4, 4) Grid (n=8,r1=10,r2=-10))")

    def testMoves(self):
        g = Grid()
        w = Walker(grid=g, start=(0,0))
        self.assertEqual(str(w),  "Walker (c=0,s=0,l=(0, 0) Grid (n=8,r1=10,r2=-10))")
        self.assertEqual(w.move(dir=DIR_S), (0,(0,1)))
        self.assertEqual(w.move(dir=DIR_S), (0,(0,2)))
        self.assertEqual(w.move(dir=DIR_S), (0,(0,3)))
        self.assertEqual(w.move(dir=DIR_S), (0,(0,4)))
        self.assertEqual(str(w),  "Walker (c=4,s=0,l=(0, 4) Grid (n=8,r1=10,r2=-10))")
        self.assertEqual(w.move(dir=DIR_E), (0,(1,4)))
        self.assertEqual(w.move(dir=DIR_E), (0,(2,4)))
        self.assertEqual(w.move(dir=DIR_E), (0,(3,4)))
        self.assertEqual(w.move(dir=DIR_E), (0,(4,4)))
        self.assertEqual(w.move(dir=DIR_E), (0,(5,4)))
        self.assertEqual(w.move(dir=DIR_E), (0,(6,4)))
        self.assertEqual(w.move(dir=DIR_E), (0,(7,4)))
        self.assertEqual(w.move(dir=DIR_E), (0,(7,4)))
        self.assertEqual(w.move(dir=DIR_E), (0,(7,4)))
        self.assertEqual(str(w),  "Walker (c=13,s=0,l=(7, 4) Grid (n=8,r1=10,r2=-10))")
        self.assertEqual(w.move(dir=DIR_S), (0,(7,5)))
        self.assertEqual(w.move(dir=DIR_S), (0,(7,6)))
        self.assertEqual(w.move(dir=DIR_S), (-10,(0,0)))
        self.assertEqual(str(w),  "Walker (c=16,s=-10,l=(0, 0) Grid (n=8,r1=10,r2=-10))")
        self.assertEqual(w.score(), -10)
        self.assertEqual(w.move(dir=DIR_N), (0,(0,0)))
        self.assertEqual(str(w),  "Walker (c=17,s=-10,l=(0, 0) Grid (n=8,r1=10,r2=-10))")
        self.assertEqual(w.score(), -10)
        self.assertEqual(w.count(), 17)

class TestQLearner(unittest.TestCase):

    def testEmptyConstructor(self):
        q = QLearner()
        self.assertEqual(q.score(),          0)
        self.assertEqual(q.count(),          0)
        self.assertEqual(q.loc(),        (0,0))
        self.assertEqual(q.epsilon(),     0.05)
        self.assertEqual(q.alpha(),        0.5)
        self.assertEqual(q.gamma(),        0.9)
        self.assertEqual(str(q),  "QLearner (a=0.500000,g=0.900000,e=0.050000,c=0,s=0.000000 None)")
        
    def testConstructor(self):    
        g = Grid()
        q = QLearner(grid=g, alpha=0.8, gamma=0.7, epsilon=0.1)
        self.assertEqual(q.score(),          0)
        self.assertEqual(q.count(),          0)
        self.assertEqual(q.loc(),        (4,4))
        self.assertEqual(q.epsilon(),      0.1)
        self.assertEqual(q.alpha(),        0.8)
        self.assertEqual(q.gamma(),        0.7)
        self.assertEqual(str(q),  "QLearner (a=0.800000,g=0.700000,e=0.100000,c=0,s=0.000000 Grid (n=8,r1=10,r2=-10))")

    def testLearning(self):
        g = Grid()
        q = QLearner(grid=g, start=(0,0))
        self.assertEqual(q.score(),          0)
        self.assertEqual(q.count(),          0)
        self.assertEqual(q.loc(),        (0,0))
        q.move(dir=DIR_S)
        q.move(dir=DIR_E)
        q.move(dir=DIR_N)
        q.move(dir=DIR_W)
        self.assertEqual(q.count(),          4)
        self.assertEqual(q.score(),         10)
        self.assertEqual(q.loc(),        (7,7))
        self.assertEqual(g[(1,0)].q(), [0.0,0.0,0.0,5.0])
        q.move(dir=DIR_W)
        q.move(dir=DIR_W)
        q.move(dir=DIR_W)
        q.move(dir=DIR_W)
        q.move(dir=DIR_W)
        q.move(dir=DIR_W)
        q.move(dir=DIR_N)
        q.move(dir=DIR_N)
        q.move(dir=DIR_N)
        q.move(dir=DIR_N)
        q.move(dir=DIR_N)
        q.move(dir=DIR_N)
        q.move(dir=DIR_N)
        q.move(dir=DIR_W)
        self.assertEqual(q.loc(),        (7,7))
        self.assertEqual(g[(1,0)].q(), [0.0,0.0,0.0,7.75])
        self.assertEqual(g[(1,1)].q(), [2.25,0.0,0.0,0.0])

    def xtest10K(self):
        g = Grid()
        q = QLearner(grid=g)
        self.assertEqual(q.score(),          0)
        self.assertEqual(q.count(),          0)
        self.assertEqual(q.loc(),        (4,4))
        for i in xrange(10000):
            q.move()
        self.assertEqual(q.count(),       10000)

class TestRollingAverage(unittest.TestCase):

    def testEmptyConstructor(self):
        r = RollingAverage()
        self.assertEqual(len(r),          0)
        self.assertEqual(r.count(),       0)
        self.assertEqual(r.n(),         200)
        self.assertEqual(r.total(),       0)
        self.assertEqual(r.average(),     0)

    def testConstructor(self):
        r = RollingAverage(n=10)
        self.assertEqual(len(r),          0)
        self.assertEqual(r.count(),       0)
        self.assertEqual(r.n(),          10)
        self.assertEqual(r.total(),       0)
        self.assertEqual(r.average(),     0)

    def testAverages(self):
        r = RollingAverage(n=10)
        self.assertEqual(len(r),          0)
        self.assertEqual(r.count(),       0)
        self.assertEqual(r.n(),          10)
        self.assertEqual(r.total(),       0)
        self.assertEqual(r.average(),     0)
        r.add(1)
        r.add(2)
        r.add(0)
        r.add(3)
        r.add(4)
        self.assertEqual(len(r),          5)
        self.assertEqual(r.count(),       5)
        self.assertEqual(r.n(),          10)
        self.assertEqual(r.total(),      10)
        self.assertEqual(r.average(),     2)
        r.add(2)
        r.add(2)
        r.add(2)
        r.add(2)
        r.add(2)
        self.assertEqual(len(r),         10)
        self.assertEqual(r.count(),      10)
        self.assertEqual(r.n(),          10)
        self.assertEqual(r.total(),      20)
        self.assertEqual(r.average(),     2)
        r.add(3)
        self.assertEqual(len(r),         10)
        self.assertEqual(r.count(),      10)
        self.assertEqual(r.n(),          10)
        self.assertEqual(r.total(),      22)
        self.assertEqual(r.average(),   2.2)
        r.add(3)
        r.add(4)
        r.add(4)
        r.add(5)
        self.assertEqual(len(r),         10)
        self.assertEqual(r.count(),      10)
        self.assertEqual(r.n(),          10)
        self.assertEqual(r.total(),      29)
        self.assertEqual(r.average(),   2.9)
        r.add(0)
        r.add(0)
        r.add(0)
        r.add(0)
        r.add(0)
        r.add(0)
        r.add(0)
        r.add(0)
        r.add(0)
        r.add(0)
        self.assertEqual(len(r),         10)
        self.assertEqual(r.count(),      10)
        self.assertEqual(r.n(),          10)
        self.assertEqual(r.total(),       0)
        self.assertEqual(r.average(),     0)
        

# --------------------------------------------------------------------
#                                                                 main
# --------------------------------------------------------------------
def main():
    print "chippy"
    unittest.main()
    #experiments(repeat=3)

# --------------------------------------------------------------------
#                                                module initialization
# --------------------------------------------------------------------
if __name__ == "__main__":
    main()
    
# ====================================================================
# end                        c h i p p y . p y                     end
# ====================================================================
