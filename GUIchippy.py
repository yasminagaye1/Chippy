import pygame, os, sys, random
from pygame.locals import *

#I DONT KNOW WHAT THIS DOES

pygame.init()


#SOME CONSTANTS

a = 0
display_width = 500
display_height = 500
box_width = 50
box_height = 50
margin = 3
locations = []
FPS = 30
fpsClock = pygame.time.Clock()

#CREATING THE FRONT END AND BACK END DISPLAYS


DISPLAY = pygame.display.set_mode((display_height, display_width))
background = pygame.Surface(DISPLAY.get_size()).convert()
pygame.display.set_caption = ('Chippy')
darkgreen = (0,80,0)

#CREATING THE 8X8 GRID
    
for row in range (8):
    for column in range (8):
        locations.append((margin + row * 53 ,margin + column * 53))

#IMAGE LOADING

chippyIMG = pygame.transform.scale(pygame.image.load("unnamed.png"), (45,50))

grassIMG = pygame.transform.scale(pygame.image.load("sgrass.jpg"), (50,50))

upIMG = pygame.transform.scale(pygame.image.load("up.png"), (45,45))

downIMG = pygame.transform.scale(pygame.image.load("down.png"), (45,45))

rightIMG = pygame.transform.scale(pygame.image.load("right.png"), (45,45))

leftIMG = pygame.transform.scale(pygame.image.load("left.png"), (45,45))

guessIMG = pygame.transform.scale(pygame.image.load("Qmark.png"), (45,45))

signIMG = pygame.transform.scale(pygame.image.load("sign.png"), (80,80))

rewardIMG = pygame.image.load("Acorn_Body.png")

regrewardIMG = pygame.transform.scale(rewardIMG, (45,50))

minirewardIMG = pygame.transform.scale(rewardIMG, (35,40))

gooIMG = pygame.image.load("1600.png")

reggooIMG = pygame.transform.scale( gooIMG , (45,50))

minigooIMG = pygame.transform.scale( gooIMG , (35,40))

#CHIPPY CONSTRUCTOR AND GRASS CONSTRUCTOR

def grass(x,y):
    background.blit(grassIMG, (x,y))

def chippy(x,y):
    background.blit(chippyIMG, (x,y))


#TEXT TO ACTION METHODS

    
def infer(x,y,direction):
    background.blit(signIMG, (420,420))
    if( direction == "G"):
        background.blit(guessIMG, (x,y))
    elif( direction == "U"):
        background.blit(upIMG, (x,y))
    elif( direction == "D"):
        background.blit(downIMG, (x,y))
    elif( direction == "R"):
        background.blit(rightIMG, (x,y))
    elif (direction == "L"):
        background.blit(leftIMG, (x,y))
def showReward(x,y,reward):
    if ( reward == "VERY LOW \n"):
        background.fill(darkgreen)
        background.blit(reggooIMG, (x,y))
    elif ( reward == "VERY HIGH \n"):
        background.fill(darkgreen)
        background.blit(regrewardIMG, (x,y))
    elif ( reward == "HIGH \m"):
        background.fill(darkgreen)
        background.blit(minirewardIMG, (x,y))
    elif ( reward == "LOW \n"):
        background.fill(darkgreen)
        background.blit(minigooIMG, (x,y))

#THE GAME LOOP

playon = True
delay = 100
background.fill(darkgreen)
DISPLAY.fill(darkgreen)
while playon:
    fpsClock.tick(FPS)
    directions = open ("/Users/chrisbanks/Desktop/WORKFILES/chippy/direct/commands.txt" , "r")
    original_location = directions.readline()
    newX=int(original_location[0]) * (margin + box_width)
    newY=int(original_location[2]) * (margin + box_height)
    for text in directions:
        oldX = newX
        oldY = newY
        if ( text[0].isalpha() ):
            infer(433,435, text[0])
        else:
            newX = int(text[0]) * ( margin + box_width)
            newY = int(text[2]) * (margin + box_height)
            grass(oldX,oldY)
            showReward(oldX, oldY, text[4:])
            chippy(newX,newY)
        DISPLAY.blit(background, (0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
