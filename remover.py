import pygame
import random
import os
import glob
import time
pygame.init()
display_width = 500
display_height = 500
box_width = 50
box_height = 50
margin = 3
locations = []

#INITIALIZATIONS FOR BUILDING THE GRASS ^^^

black = (0,0,0)
white = (255,255,255)
darkgreen = (0,80,0)
green = (0,100,0)

#COLORS THAT ARE USED ^^^

guess = pygame.image.load("Qmark.png")
upArrow = pygame.image.load("up.png")
downArrow = pygame.image.load("down.png")
rightArrow = pygame.image.load("right.png")
leftArrow = pygame.image.load("left.png")
gameDisplay = pygame.display.set_mode((display_width,display_height))
grass_image = pygame.image.load("sgrass.jpg" )
grass_image = pygame.transform.scale( grass_image, (50,50))
goo_image = pygame.image.load("1600.png")
goo_image = pygame.transform.scale( goo_image , (45,50))
small_goo_image = pygame.transform.scale(goo_image , (35,40))
reward_image = pygame.image.load("Acorn_Body.png")
reward_image = pygame.transform.scale(reward_image, (45,50))
small_reward_image = pygame.transform.scale( reward_image, (35,40))
chippyImg = pygame.image.load("unnamed.png")
chippyImg = pygame.transform.scale( chippyImg, (45,50))

#IMAGES THAT ARE USED ^^^

for row in range (18):
    for column in range (18):
        locations.append((margin + row * 53 ,margin + column * 53))

#ADDING THE SQUARES TO THE LOCATIONS ARRAY

def upArrow(x,y):
    gameDisplay.blit( guess , (x,y) )
def downArrow(x,y):
    gameDisplay.blit( downArrow , (x,y) )
def rightArrow(x,y):
    gameDisplay.blit( rightArrow , (x,y) ) 
def leftArrow(x,y):
    gameDisplay.blit( leftArrow , (x,y) )
def guess(x,y):
    gameDisplay.blit( guess , (x,y) ) 
def goo(x,y):
    gameDisplay.blit(goo_image, (x,y) )
def minigoo(x,y):
    gameDisplay.blit(small_goo_image , (x,y))
def grass (x,y):
    gameDisplay.blit(grass_image, (x,y) )
def chippy(x,y):
    gameDisplay.blit(chippyImg, (x,y) )
def minireward(x,y):
    gameDisplay.blit(small_reward_image, (x,y))
def reward(x,y):
    gameDisplay.blit(reward_image, (x,y) )

#OBJECT CONSTRUCTORS ^^^

def game_loop():
    #reward_loc = locations[random.randint(0,100)]
    #chippy_loc = locations[random.randint(0,100)]
    #goo_loc = locations[random.randint(0,100)]
    #x = chippy_loc[0]
    #y = chippy_loc[1]
    #x_change = 0
    #y_change = 0
    #delay = 150
    pygame.display.set_caption('Chippy on a Grid')
    #clock = pygame.time.Clock()
    playon = True
    while playon:
        gameDisplay.fill(darkgreen)                                                     
        #clock.tick(60)
