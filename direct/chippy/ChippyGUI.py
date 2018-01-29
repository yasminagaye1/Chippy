import pygame
import random
import os
import glob
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
reward_image = pygame.image.load("Acorn_Body.png")
reward_image = pygame.transform.scale(reward_image, (45,50))
chippyImg = pygame.image.load("unnamed.png")
chippyImg = pygame.transform.scale( chippyImg, (45,50))
files = glob.glob("/Users/chrisbanks/Desktop/WORKFILES/chippy/direct/*.txt")
for row in range (18):
    for column in range (18):
        locations.append((margin + row * 53 ,margin + column * 53))
def goo(x,y):
    gameDisplay.blit(goo_image, (x,y) )
def grass (x,y):
    gameDisplay.blit(grass_image, (x,y) )
def chippy(x,y):
    gameDisplay.blit(chippyImg, (x,y) )
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
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                playon = True
#            if event.type == pygame.KEYDOWN:
#                if event.key == pygame.K_LEFT and x > 3:
#                    x_change = -53
#                    pygame.time.wait(delay)
#                elif event.key == pygame.K_RIGHT and x < 480:
#                    x_change = 53
#                    pygame.time.wait(delay)
#                elif event.key == pygame.K_UP and y > 3:
#                    y_change = -53
#                    pygame.time.wait(delay)
#                elif event.key == pygame.K_DOWN and y < 480:
#                    y_change = 53
#                    pygame.time.wait(delay)
#            if event.type == pygame.KEYUP:
#                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
#                    x_change = 0;
#                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
#                    y_change = 0
        gameDisplay.fill(darkgreen)
#        for row in range(18):
#            for column in range(18):
#                color = green
#                pygame.draw.rect(gameDisplay, color, [(margin + box_width) * column + margin,
#                                                      (margin + box_height) * row + margin,
#                                                      box_width, box_height])
        clock.tick(60)
        
        directions = open ("/Users/chrisbanks/Desktop/WORKFILES/chippy/direct/commands.txt" , "r")
        original_location = directions.readline()
        newX=int(original_location[0]) * (margin + box_width)
        newY=int(original_location[2]) * (margin + box_height)
        for text in directions:
            oldX = newX
            oldY =  newY
            newX = int(text[0]) * ( margin + box_width)
            newY = int(text[2]) * (margin + box_height)
            if text[4:] == "VERY LOW \n":
                grass(oldX,oldY)
                gameDisplay.fill(darkgreen)
                goo(oldX,oldY)
                print ("goo")
            elif text[4:] == "VERY HIGH \n":
                grass(oldX,oldY)
                gameDisplay.fill(darkgreen)
                reward(oldX,oldY)
                print ("acorn")
            else:
                grass ( oldX, oldY)
            chippy(newX , newY)
#            if text[0] == "0" and y > 3:
#               print (text)
#               grass(x,y)
#               y_change = -53
#               y += y_change
#               pygame.time.wait(delay)
#            elif text[0] == "1" and y < 480:
#                print (text)
#                grass(x,y)
#                y_change = 53
#                y += y_change
#                pygame.time.wait(delay)
#            elif text[0] == "2" and x > 3:
#                print (text)
#                grass(x,y)
#                x_change = -53
#                x += x_change
#                pygame.time.wait(delay)
#            elif text[0] == "3" and x < 480:
#                print (text)
#                grass(x,y)
#                x_change = 53
#                x += x_change
            print ("\"" ,text[4:],"\"")
            pygame.time.wait(delay)
            pygame.display.update()
game_loop()
pygame.quit()
quit()

