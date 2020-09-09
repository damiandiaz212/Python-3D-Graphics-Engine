import pygame
import math
from datetime import datetime
from Scripts.graphicsEngine3d import GraphicsEngine
from Scripts.geometry import Mesh
from Lib.colors import *


# initialize pygame
pygame.init()
width = 800
height = 600

# window setup
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Python 3D Graphics Engine")
icon = pygame.image.load('icons/cube.png')
pygame.display.set_icon(icon)

# initialize graphics engine
engine = GraphicsEngine(width, height)
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
    theta = (currentTick - lastTick) / 600
    lastTick = currentTick

    # call engine
    # to view wireframe add the arg True
    engine.on_user_update(screen, theta)

    # update screen
    pygame.display.update()


  
    

