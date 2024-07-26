import pygame
import os

MAIN_DIRECTORY = os.path.dirname(__file__)
MAIN_DIRECTORY = os.path.dirname(MAIN_DIRECTORY)

ASSETS_DIRECTORY = os.path.join(MAIN_DIRECTORY, 'assets')
SRC_DIRECTORY = os.path.join(MAIN_DIRECTORY, 'src')

MAPS_DIRECTORY = os.path.join(ASSETS_DIRECTORY, 'maps')
SPRITES_DIRECTORY = os.path.join(ASSETS_DIRECTORY, 'sprites')
TILES_DIRECTORY = os.path.join(ASSETS_DIRECTORY, 'tiles')
