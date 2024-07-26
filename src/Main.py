import pygame
from Game import *
from Phase import *
from Map import *
import os
from Paths import *
from sys import exit 

framerate = pygame.time.Clock()

SCREEN_HEIGHT = 1200
SCREEN_WIDTH = 700

screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
pygame.display.set_caption("Mini-Golf Mania")
pygame.display.set_icon(pygame.image.load(os.path.join(ASSETS_DIRECTORY, 'golf_icon.png')))

map = Map(os.path.join(MAPS_DIRECTORY, 'fase_1.csv'))
fase = Phase(map)
game = Game(fase, screen)

while True:
    screen.fill('black')
    framerate.tick(30)
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           exit()
    
    game.draw(screen)
    game.update()
    pygame.display.flip()