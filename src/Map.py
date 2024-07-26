import pygame
from Obstacle import *
from Ball import *
from Util import *
from sys import exit
from Paths import *
import os

# Tiles
GRASS = 0
RIVER_RIGHT = 1
RIVER_UP = 2
RIVER_DOWN = 3
RIVER_LEFT = 4
RIVER_DIAGONAL_UL = 5
RIVER_DIAGONAL_BL   = 6
RIVER_DIAGONAL_BR = 7
RIVER_DIAGONAL_UR = 8

# Obstáculos
WALL_STRAIGHT = 9
WALL_SPIN_LIGHT = 10
WALL_SPIN_SHADOW = 11
WALL_STOP_UP = 12
WALL_STOP_DOWN = 13
DYNAMIC_WALL_HORIZONTAL = 14
DYNAMIC_WALL_VERTICAL = 15
LAGOON = 16
SLIME = 17
FAN = 18

# Buraco
HOLE = 19

# Bola
BALL = 20

# Para ordenar o grupo de sprites de obstáculo
def get_class_priority(sprite):
    if isinstance(sprite, StaticObstacle):
        return 1
    elif isinstance(sprite, StaticAnimatedObstacle):
        return 2
    elif isinstance(sprite, DynamicObstacle):
        return 3
    else:
        return 4  # Para outros tipos de sprites

class StaticTile(pygame.sprite.Sprite):
    # Construtor
    def __init__(self,
                 position: tuple[int, int], 
                 sprite: pygame.Surface) -> None:
        super().__init__()
        # Atributos privados
        self.__position = position

        # Atributos públicos necessários da classe Sprite
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.__position[0], self.__position[1])

class DynamicTile(pygame.sprite.Sprite):
    # Construtor
    def __init__(self,  
                 position: pygame.Vector2, 
                 sprite_list: list[pygame.Surface]) -> None:
        super().__init__()
        # Atributos privados
        self.__position = position
        self.__sprite_list = sprite_list
        self.__animation_FrameIndex = 0

        # Atributos públicos necessários da classe Sprite
        self.image = self.__sprite_list[self.__animation_FrameIndex]
        self.rect = self.image.get_rect()
        self.rect.topleft = (int(self.__position.x), int(self.__position.y))

        # Constantes privadas
        self.__FRAMERATE = 0.16

    def update(self) -> None:
        self.__animation_FrameIndex += self.__FRAMERATE
        
        if(self.__animation_FrameIndex > len(self.__sprite_list)):
            self.__animation_FrameIndex = 0
        
        self.image = self.__sprite_list[int(self.__animation_FrameIndex)]

class Map:
    # Construtor
    def __init__(self, 
                 mapfile: str) -> None:
        # Atributos públicos
        self.tilesGroup = pygame.sprite.Group()
        self.obstaclesGroup = pygame.sprite.Group()
        self.hole = pygame.sprite.GroupSingle()
        self.ball = pygame.sprite.GroupSingle()
        self.loadMap(mapfile)

    # Carrega o mapa de uma matriz definida em um arquvivo CSV
    def loadMap(self, filename: str) -> None:
        mapa = read_matrix_from_file(os.path.join(ASSETS_DIRECTORY, 'maps', filename))
        img = None
        for y, row in enumerate(mapa):
            for x, tile_index in enumerate(row):

                # Caso seja um tile
                if tile_index <= 8:
                    img = read_one_from_spritesheet(os.path.join(TILES_DIRECTORY, 'floor.png'), tile_index, 0)
                    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                    self.tilesGroup.add(StaticTile((x * TILE_SIZE, y * TILE_SIZE), img))

                # Caso seja um obstáculo ou o buraco
                else:
                    if tile_index <= 13:
                        img = read_one_from_spritesheet(os.path.join(SPRITES_DIRECTORY, 'walls.png'), 0, tile_index-9)
                        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                        self.obstaclesGroup.add(StaticObstacle(img, (x * TILE_SIZE, y * TILE_SIZE), tile_index))

                    elif tile_index == DYNAMIC_WALL_HORIZONTAL:
                        # Grama de fundo
                        img = read_one_from_spritesheet(os.path.join(TILES_DIRECTORY, 'floor.png'), 0, 0)
                        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                        self.tilesGroup.add(StaticTile((x * TILE_SIZE, y * TILE_SIZE), img))
                        # Parede
                        img = read_one_from_spritesheet(os.path.join(SPRITES_DIRECTORY, 'dwalls.png'), 0, 0)
                        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                        self.obstaclesGroup.add(DynamicObstacle(img, pygame.Vector2(x * TILE_SIZE, y * TILE_SIZE), 
                                                                pygame.Vector2(2.5,0),
                                                                (x * TILE_SIZE + TILE_SIZE * 2, y * TILE_SIZE), (x * TILE_SIZE - TILE_SIZE * 2, y * TILE_SIZE),
                                                                tile_index))
                    
                    elif tile_index == DYNAMIC_WALL_VERTICAL:
                        # Grama de fundo
                        img = read_one_from_spritesheet(os.path.join(TILES_DIRECTORY, 'floor.png'), 0, 0)
                        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                        self.tilesGroup.add(StaticTile((x * TILE_SIZE, y * TILE_SIZE), img))
                        # Parede
                        img = read_one_from_spritesheet(os.path.join(SPRITES_DIRECTORY, 'dwalls.png'), 0, 1)
                        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                        self.obstaclesGroup.add(DynamicObstacle(img, pygame.Vector2(x * TILE_SIZE, y * TILE_SIZE), 
                                                                pygame.Vector2(0,2.5),
                                                                (x * TILE_SIZE, y * TILE_SIZE + TILE_SIZE * 2), (x * TILE_SIZE, y * TILE_SIZE - TILE_SIZE * 2),
                                                                tile_index))

                    elif tile_index == LAGOON:
                        sprites = read_all_from_spritesheet(os.path.join(SPRITES_DIRECTORY, 'lagoon.png'), 3, 3)
                        sprites.pop()
                        for i in range(len(sprites)):
                            sprites[i] = pygame.transform.scale(sprites[i], (TILE_SIZE, TILE_SIZE))
                        self.obstaclesGroup.add(StaticAnimatedObstacle(sprites, (x * TILE_SIZE, y * TILE_SIZE), tile_index))

                    elif tile_index == SLIME:
                        # Grama de fundo
                        img = read_one_from_spritesheet(os.path.join(TILES_DIRECTORY, 'floor.png'), 0, 0)
                        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                        self.tilesGroup.add(StaticTile((x * TILE_SIZE, y * TILE_SIZE), img))
                        # Slime
                        img = read_one_from_spritesheet(os.path.join(SPRITES_DIRECTORY, 'slime.png'), 0, 0)
                        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                        self.obstaclesGroup.add(StaticObstacle(img, (x * TILE_SIZE, y * TILE_SIZE), tile_index))

                    # elif tile_index == FAN:
                    #     sprites = read_all_from_spritesheet(os.path.join(SPRITES_DIRECTORY, 'abismo.png'), 3, 3, (32, 32))

                    elif tile_index == HOLE:
                        # Grama de fundo
                        img = read_one_from_spritesheet(os.path.join(TILES_DIRECTORY, 'floor.png'), 0, 0)
                        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                        self.tilesGroup.add(StaticTile((x * TILE_SIZE, y * TILE_SIZE), img))
                        # Bandeira
                        sprites = read_all_from_spritesheet(os.path.join(SPRITES_DIRECTORY, 'flag.png'), 2, 4)
                        sprites.pop()
                        for i in range(len(sprites)):
                            sprites[i] = pygame.transform.scale(sprites[i], (TILE_SIZE, TILE_SIZE))
                        self.tilesGroup.add(StaticAnimatedObstacle(sprites, (x * TILE_SIZE - 10, y * TILE_SIZE - 35), tile_index))
                        # BURACO
                        img = read_one_from_spritesheet(os.path.join(SPRITES_DIRECTORY, 'hole.png'), 0, 0)
                        self.hole.add(StaticObstacle(img, (x * TILE_SIZE, y * TILE_SIZE), tile_index))

                    elif tile_index == BALL:
                        # Grama de fundo
                        img = read_one_from_spritesheet(os.path.join(TILES_DIRECTORY, 'floor.png'), 0, 0)
                        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                        self.tilesGroup.add(StaticTile((x * TILE_SIZE, y * TILE_SIZE), img))
                        # Bola
                        sprites = read_all_from_spritesheet(os.path.join(SPRITES_DIRECTORY, 'ball.png'), 3, 3)
                        sprites.pop()
                        for i in range(len(sprites)):
                            sprites[i] = pygame.transform.scale(sprites[i], (TILE_SIZE, TILE_SIZE))
                        self.ball.add(Ball(sprites, pygame.Vector2(x * TILE_SIZE, y * TILE_SIZE)))
        
        self.obstaclesGroup = pygame.sprite.Group(sorted(self.obstaclesGroup, key=get_class_priority))

    # Desenha o mapa e os obstáculos
    def draw(self, screen: pygame.Surface):
        self.tilesGroup.draw(screen)
        self.obstaclesGroup.draw(screen)
        self.hole.draw(screen)
        self.ball.draw(screen)

    # Atualiza o mapa e os obstáculos
    def update(self):
        self.tilesGroup.update()
        self.obstaclesGroup.update()
        self.ball.update()
