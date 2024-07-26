import pygame
import os
from Util import *
from Paths import *
from Map import *
from Obstacle import *
from Ball import *

class Phase:
    def __init__(self, map: Map) -> None:
        self.__map = map
        self.__force_bar = pygame.image.load(os.path.join(SPRITES_DIRECTORY, 'bar.png'))
        self.__drawingPlay = False
        self.__vec_move_start = pygame.Vector2(-1, -1)
        self.__vec_move_end = pygame.Vector2(-1, -1)
        self.winner = False
    
    def draw(self, screen: pygame.Surface):
        self.__map.draw(screen)
        if self.__drawingPlay:
            draw_arrow(screen, pygame.Color(80, 245, 191), pygame.Vector2(pygame.mouse.get_pos()), self.__map.ball.sprite.get_position())
            #MEDIDOR

    def update(self):
        self.__map.update()
        self.check_collisions()
        
        mouse_clicked = pygame.mouse.get_pressed()[0]
        if mouse_clicked and self.__map.ball.sprite.is_colliding(pygame.mouse.get_pos()) or self.__drawingPlay:
            self.__vec_move_start = self.__map.ball.sprite.get_position()
            self.__drawingPlay = True
        if not mouse_clicked:
            self.__vec_move_end = pygame.Vector2(pygame.mouse.get_pos())
            self.__drawingPlay = False

        if self.__vec_move_start != pygame.Vector2(-1,-1) and self.__vec_move_end != pygame.Vector2(-1,-1) and not pygame.mouse.get_pressed()[0]:
            force = self.__vec_move_end - self.__vec_move_start
            force.x = abs(force.x)
            force.y = abs(force.y)
            self.__map.ball.sprite.make_move(self.__vec_move_start - self.__vec_move_end, force/10)
            self.__vec_move_start = pygame.Vector2(-1,-1)
            self.__vec_move_end = pygame.Vector2(-1,-1)

    # def timer(self, x, y, screen):  #Tempo rolando enquanto rola a fase
    #     font = pygame.font.SysFont('comic sans', 40, True, False)
    #     time = (pygame.time.get_ticks() - 0) / 1000
    #     text = font.render(f"Tempo: {time}", True, (255, 255, 255))
    #     textRect = text.get_rect()
    #     textRect.topleft = (x, y)
    #     screen.blit(text, textRect)

    # Checa colisões entre os grupos de sprite
    def check_collisions(self):
        collisions = pygame.sprite.spritecollide(self.__map.ball.sprite, self.__map.obstaclesGroup, False, pygame.sprite.collide_mask)
        
        for object_collided in collisions:
            if object_collided.ID == LAGOON:
                self.__map.ball.sprite.fall()
                
            if object_collided.ID == SLIME:
                self.__map.ball.sprite.stuck()

            if object_collided.ID == HOLE:
                self.winner = True

            if object_collided.ID <= DYNAMIC_WALL_VERTICAL:
                A = self.__map.ball.sprite.rect
                B = object_collided.rect

                b_collision = B.bottom - A.center[1];
                t_collision = A.bottom - B.center[1];
                l_collision = A.right - B.center[0];
                r_collision = B.right - A.center[0];

                if (t_collision < b_collision and t_collision < l_collision and t_collision < r_collision ):
                    #Top collision
                    self.__map.ball.sprite.invert_y_speed()
                if (b_collision < t_collision and b_collision < l_collision and b_collision < r_collision):
                    # bottom collision
                    self.__map.ball.sprite.invert_y_speed()
                if (l_collision < r_collision and l_collision < t_collision and l_collision < b_collision):
                    #Left collision
                    self.__map.ball.sprite.invert_x_speed()
                if (r_collision < l_collision and r_collision < t_collision and r_collision < b_collision):
                    #Right collision
                    self.__map.ball.sprite.invert_x_speed()
