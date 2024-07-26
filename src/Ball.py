import pygame
from Util import TILE_SIZE
import math

class Ball(pygame.sprite.Sprite):
    # Construtor
    def __init__(self,
                 sprite_list: list[pygame.Surface],
                 position: pygame.Vector2) -> None:
        super().__init__()
        self.__position = position + pygame.Vector2(TILE_SIZE//2, TILE_SIZE//2)
        self.__radius = 9
        self.speed = pygame.Vector2(0, 0)
        self.__acceleration = pygame.Vector2(0,0)
        self.__sprite_list = sprite_list
        self.__animation_FrameIndex = 0
        self.__isFalling = False
        self.__scaleFalling = 0.01
        self.__timer = 0
        
        # Constantes privadas da cinemática
        self.ACCELERATION = 20  # O que rápido o obejto acelera
        self.FRICTION = 0.05    # 'Desaceleração'
        # Constante de taxa de ataulização da animação
        self.__FRAMERATE = 0.16

        # Atributos públicos necessários da superclasse Sprite
        self.image = sprite_list[0]
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.__position.x), int(self.__position.y))

    def is_colliding(self, point: tuple[int, int]):
        distance = math.sqrt((self.__position.x - point[0])**2 + (self.__position.y - point[1])**2)
        return distance <= self.__radius

    def get_position(self) -> pygame.Vector2:
        return self.__position
    
    def set_position(self, newPosition: pygame.Vector2):
        self.__position = newPosition
        self.rect.center = (round(newPosition.x), round(newPosition.y))

    def invert_y_speed(self):
        self.speed.y *= -1

    def invert_x_speed(self):
        self.speed.x *= -1

    def make_move(self, vec: pygame.Vector2, force: pygame.Vector2):
        self.__acceleration.x = force.x * math.copysign(1, vec.x * self.ACCELERATION)
        self.__acceleration.y = force.y * math.copysign(1, vec.y * self.ACCELERATION)
        self.speed += self.__acceleration

    def fall(self):
        self.__isFalling = True
        self.__timer = (pygame.time.get_ticks() - 0) / 1000
    
    def stuck(self):
        self.FRICTION *= 10

    def release(self):
        self.FRICTION /= 10

    def isStatic(self) -> bool:
        return self.speed.y < 0.005 and self.speed.x < 0.005


    def update(self):
        # Calculo da aceleração (t = 1) com escalar de fricção:
        self.__acceleration =  (-self.speed) * self.FRICTION
        # Calculo da velocidade a partir da aceleração (t = 1): 
        self.speed += self.__acceleration

        # Calculo da posição final a partir da aceleração:
        self.__position += self.speed + 0.5 * self.__acceleration
        self.rect.center = (round(self.__position.x), round(self.__position.y))

        if not self.isStatic() and not self.__isFalling:
            self.__animation_FrameIndex += self.__FRAMERATE
        
            if(self.__animation_FrameIndex > len(self.__sprite_list)):
                self.__animation_FrameIndex = 0
            
            self.image = self.__sprite_list[int(self.__animation_FrameIndex)]
        
        if self.__isFalling:
            self.image = pygame.transform.scale(self.image, (TILE_SIZE * self.__scaleFalling, TILE_SIZE * self.__scaleFalling))
            self.__scaleFalling += 0.01
            over = ((pygame.time.get_ticks() - 0) / 1000) - self.__timer
            if self.__timer >= 3:
                self.__isFalling = False

