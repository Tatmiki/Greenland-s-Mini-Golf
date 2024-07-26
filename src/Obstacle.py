import pygame

class DynamicObstacle(pygame.sprite.Sprite):
    # Construtor
    def __init__(self, 
                 sprite: pygame.Surface,
                 position: pygame.Vector2, 
                 velocity: pygame.Vector2, 
                 target_A: tuple[int, int], 
                 target_B: tuple[int, int],
                 ID: int) -> None:
        super().__init__()
        # Atributos protegidos
        self.__position = position
        self.__velocity = pygame.Vector2(velocity)
        self.__target_A = target_A
        self.__target_B = target_B
        self.__verification = True
        self.ID = ID

        # Atributos públicos necessários da superclasse Sprite
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = (int(self.__position.x), int(self.__position.y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.__velocity.x != 0:
            if self.__position.x < self.__target_A[0] and self.__verification:
                self.__position += self.__velocity
            if self.__position.x >= self.__target_A[0]:
                self.__verification = False
            if self.__position.x > self.__target_B[0] and not self.__verification:
                self.__position -= self.__velocity
            if self.__position.x <= self.__target_B[0]:
                self.__verification = True
                
        if self.__velocity.y != 0:    
            if self.__position.y < self.__target_A[1] and self.__verification:
                self.__position += self.__velocity
            if (self.__position.y) >= self.__target_A[1]:
                self.__verification = False
            if self.__position.y > self.__target_B[1] and not self.__verification:
                self.__position -= self.__velocity
            if self.__position.y <= self.__target_B[1]:
                self.__verification = True
         
        self.rect.topleft = (int(self.__position.x), int(self.__position.y))

class StaticObstacle(pygame.sprite.Sprite):
    # Construtor
    def __init__(self, 
                 sprite: pygame.Surface,
                 position: tuple[int, int],
                 ID: int):
        super().__init__()
        # Atributos protegidos
        self._position = position
        self.ID = ID

        # Atributos públicos necessários da classe Sprite
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = (self._position[0], self._position[1])
        self.mask = pygame.mask.from_surface(self.image)

class StaticAnimatedObstacle(StaticObstacle):
    def __init__(self, 
                 sprite_list: list[pygame.Surface],
                 position: tuple[int, int],
                 ID: int):
        super().__init__(sprite_list[0], position, ID)
        self.__sprite_list = sprite_list
        self.__animation_FrameIndex = 0
        self.ID = ID

        # Constantes privadas
        self.__FRAMERATE = 0.16

    def update(self) -> None:
        self.__animation_FrameIndex += self.__FRAMERATE
        
        if(self.__animation_FrameIndex > len(self.__sprite_list)):
            self.__animation_FrameIndex = 0
        
        self.image = self.__sprite_list[int(self.__animation_FrameIndex)]
