import pygame
import math
from datetime import datetime
from Scripts.graphicsEngine3d import ge3d
from Lib.colors import *


"""

main.py
author: Damian Diaz

defines and initializes the graphicsEngine3d and pygame window

"""

# initialize pygame
pygame.init()
width = 800
height = 600

# window setup
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Graphics Engine")
icon = pygame.image.load('cube_blue.png')
pygame.display.set_icon(icon)

# initialize graphics engine
engine = ge3d(width, height)
engine.on_user_create()

lastTick = pygame.time.get_ticks()
currentTick = 0
theta = 0
    
# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # reset screen
    screen.fill(black)

    # updating our theta time
    currentTick = pygame.time.get_ticks()
    theta = (currentTick - lastTick) / 500
    lastTick = currentTick

    # call engine
    engine.on_user_update(screen, theta)

    # update screen
    pygame.display.update()

  
    

