import pygame, os, sys, random
from pygame.locals import *

#I DONT KNOW WHAT THIS DOES



class GUIchippy(object):   
#SOME CONSTANTS
    
    def __init__(self):
        pygame.init()
        self.__a = 0, 
        self.__display_width = 500
        self.__display_height = 500
        self.__box_width = 50
        self.__box_height = 50
        self.__margin = 3
        self.__locations = []
        self.__FPS = 30
        self.__DISPLAY = pygame.display.set_mode((self.__display_height, self.__display_width))
        self.__fpsClock = pygame.time.Clock()
        #self.__background
        #DISPLAY FUNCTIOM
        self.__darkgreen = (0,80,0)
        self.__white = (255, 255, 255)
        self.__red = (255, 0, 0)
        #CREATING THE FRONT END AND BACK END DISPLAYS
        self.__DISPLAY = pygame.display.set_mode((self.__display_height, self.__display_width))
        self.__background = pygame.Surface(self.__DISPLAY.get_size()).convert()
        self.__background.fill(self.__darkgreen)
        self.__DISPLAY.fill(self.__darkgreen)
        pygame.display.set_caption = ('Chippy')
       
        #CREATING THE 8X8 GRID     
        for row in range (8):
            for column in range (8):
                 self.__locations.append((self.__margin + row * 53 , self.__margin + column * 53)) 
        self.__playon = True
        self.__delay = 100
        
   
        #IMAGE LOADING
        self.__chippyIMG = pygame.transform.scale(pygame.image.load("unnamed.png"), (45,50))
        
        self.__grassIMG = pygame.transform.scale(pygame.image.load("sgrass.jpg"), (50,50))
        
        self.__upIMG = pygame.transform.scale(pygame.image.load("up.png"), (45,45))
        
        self.__downIMG = pygame.transform.scale(pygame.image.load("down.png"), (45,45))
        
        self.__rightIMG = pygame.transform.scale(pygame.image.load("right.png"), (45,45))
        
        self.__leftIMG = pygame.transform.scale(pygame.image.load("left.png"), (45,45))
        
        self.__guessIMG = pygame.transform.scale(pygame.image.load("Qmark.png"), (45,45))
        
        self.__signIMG = pygame.transform.scale(pygame.image.load("sign.png"), (80,80))
        
        self.__rewardIMG = pygame.image.load("Acorn_Body.png")
        
        self.__rewardIMG2 = pygame.image.load("redNutt.jpg")
        
        self.__regrewardIMG = pygame.transform.scale(self.__rewardIMG, (45,50))
        
        self.__regrewardIMG2 = pygame.transform.scale(self.__rewardIMG2, (45,50))
        
        self.__minirewardIMG = pygame.transform.scale(self.__rewardIMG, (35,40))
        
        self.__gooIMG = pygame.image.load("1600.png")
        
        self.__reggooIMG = pygame.transform.scale( self.__gooIMG , (45,50))
        
        self.__minigooIMG = pygame.transform.scale( self.__gooIMG , (35,40))
        #UPDSIPLAY FUNCTION
  
    #CHIPPY CONSTRUCTOR AND GRASS CONSTRUCTOR
    #function to set the grass
    def grass(self, x,y):
        self.__background.blit(self.__grassIMG, (x,y))
    
    #function to visual chippy
    def chippy(self, x,y):
        self.__background.blit(self.__chippyIMG, (x,y))
    
    #function to set the reward images
    def rewardI (self, x,y):
        self.__background.blit(self.__regrewardIMG, (x,y))
        
    def rewardI2 (self, x,y):
        self.__background.blit(self.__regrewardIMG2, (x,y))
        
    #TEXT TO ACTION METHODS    
    def infer(self, x,y, direction):
        self.__background.blit(self.__signIMG, (420,420))
        if( direction == "G"):
            self.__background.blit(self.__guessIMG, (x,y))
        elif( direction == "U"):
            self.__background.blit(self.__upIMG, (x,y))
        elif( direction == "D"):
            self.__background.blit(self.__downIMG, (x,y))
        elif( direction == "R"):
            self.__background.blit(self.__rightIMG, (x,y))
        elif (direction == "L"):
            self.__background.blit(self.__leftIMG, (x,y))
            
    def showReward(self, x,y,reward):
        if (reward == "VERY LOW"):
            self.__background.fill(self.__darkgreen)
            self.__background.blit(self.__regrewardIMG, (x,y))
        elif ( reward == "MEDIUM"):
            self.__background.fill(self.__darkgreen)
            self.__background.blit(self.__regrewardIMG, (x,y))
        elif ( reward == "VERY HIGH"):
            self.__background.fill(self.__darkgreen)
            self.__background.blit(self.__regrewardIMG, (x,y))
        elif ( reward == "HIGH"):
            self.__background.fill(self.__darkgreen)
            self.__background.blit(self.__regrewardIMG, (x,y))
        elif ( reward == "LOW"):
            self.__background.fill(self.__darkgreen)
            self.__background.blit(self.__regrewardIMG, (x,y))

            
       #gUIchippy function
    def gUIchippy(self, original_location, count):
        #communicate with grid
        self.__fpsClock.tick(self.__FPS)
       
        print ("This is original location", original_location)
        newX=int(original_location[0][0]) * (self.__margin + self.__box_width)
        newY=int(original_location[0][2]) * (self.__margin + self.__box_height)
        #for text in directions:
        oldX = newX
        oldY = newY
        newX = int(original_location[0][0]) * ( self.__margin + self.__box_width)
        newY = int(original_location[0][2]) * (self.__margin + self.__box_height)
        #self.grass(oldX,oldY)
        self.showReward(oldX, oldY, original_location[1])
        
        #Locations of the 2 rewards
        rewardX = 0 * (self.__margin + self.__box_width)
        rewardY = 0 * (self.__margin + self.__box_height)
        rewardX2 = 7 * (self.__margin + self.__box_width)
        rewardY2= 7 * (self.__margin + self.__box_height)
        
        #SWITCH THE THE POSITIVE AND NEGATIVE REWARD IMAGE EVERY 10,000 STEPS
        if count < 10000:
            self.rewardI(rewardX, rewardY)
            self.rewardI2(rewardX2, rewardY2)
        else:
            self.rewardI(rewardX2, rewardY2)
            self.rewardI2(rewardX, rewardY)
        
        self.infer(433,435, original_location[2][0])
        self.grass(oldX,oldY)
        self.chippy(newX,newY)
        
        self.__DISPLAY.blit(self.__background, (0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                playon = False
                
    #def showThoughts(self, inference):
        #return inference
    
    