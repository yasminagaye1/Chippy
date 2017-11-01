import pygame
import random
import os
import time
pygame.init()
display_width = 500
display_height = 500
shouldRestart = False
box_width = 50
box_height = 50
margin = 3
locations = []
black = (0,0,0)
white = (255,255,255)
darkgreen = (0,80,0)
green = (0,100,0)
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
for row in range (18):
    for column in range (18):
        locations.append((margin + row * 53 ,margin + column * 53))
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
def game_loop():
    reward_loc = locations[random.randint(0,100)]
    chippy_loc = locations[random.randint(0,100)]
    goo_loc = locations[random.randint(0,100)]
    x = chippy_loc[0]
    y = chippy_loc[1]
    x_change = 0
    y_change = 0
    delay = 150
    pygame.display.set_caption('Chippy on a Grid')
    clock = pygame.time.Clock()
    playon = True
    while playon:
        gameDisplay.fill(darkgreen)                                                     
        clock.tick(60)
        directions = open ("commands.txt" , "r")
        original_location = directions.readline()
        newX=int(original_location[0]) * (margin + box_width)
        newY=int(original_location[2]) * (margin + box_height)
        for text in directions:
            oldX = newX
            oldY =  newY
            newX = int(text[0]) * ( margin + box_width)
            newY = int(text[2]) * (margin + box_height)
            if text[4:] == "VERY LOW \n":
                gameDisplay.fill(darkgreen)
                goo(oldX,oldY)
                print ("goo")
            elif text[4:] == "VERY HIGH \n":
                gameDisplay.fill(darkgreen)
                reward(oldX,oldY)
                print ("acorn")
            elif text[4:] == "HIGH \n":
                gameDisplay.fill(darkgreen)
                minireward(oldX,oldY)
                print ("mini acorn")
            elif text[4:] == "LOW \n":
                gameDisplay.fill(darkgreen)
                minigoo(oldX,oldY)
            else:
                grass ( oldX, oldY)
            chippy(newX , newY)
            print (text[4:])
#            pygame.time.wait(delay)
            pygame.display.update()
game_loop()
pygame.quit()
quit()

