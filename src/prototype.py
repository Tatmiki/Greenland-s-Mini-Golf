import pygame
from pygame.locals import *
from sys import exit
import math
from Util import draw_arrow

pygame.init()

# Declaração da tela e do seu tamanho
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Protótipo")

# Declaraão da atualização 
timer = pygame.time.Clock()    

# Vetor originário
vector = pygame.math.Vector2

# Classe

# Classe e Variávels da bola
class Ball:
    def __init__(self):
        self.position = vector(400, 300)    # Posição da bola
        self.acceleration = vector(0,0)     # Modificador da velo1cidade
        self.velocity = vector(0,0)         # Movimento
        self.ball_radius = 20

        # Constantes cinemáticas
        self.ACCELERATION = 20  # O que rápido o obejto acelera
        self.FRICTION = 0.05    # 'Desaceleração'

    def is_colliding(self, point):
        px, py = point
        distance = math.sqrt((self.position.x - px)**2 + (self.position.y - py)**2)
        return distance <= self.ball_radius

    def swap_move_y(self):
        self.velocity.y *= -1

    def swap_move_x(self):
        self.velocity.x *= -1

    def make_move(self, vec, force):
        self.acceleration.x = force.x * math.copysign(1, vec.x * self.ACCELERATION)
        self.acceleration.y = force.y * math.copysign(1, vec.y * self.ACCELERATION)
        self.velocity += self.acceleration

    def update(self): # Movimentação da bola - Mouse
        #self.acceleration = vector(0, 0)

        # Calculado a cinemática
        self.acceleration =  (-self.velocity) * self.FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

ball = Ball()
vec_move_start = vector(-1,-1)
vec_move_end = vector(-1.-1)

# arrow
drawing_arrow = False

# Operações que ocorrem quando o jogo está aberto
while True:
    timer.tick(30)
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == QUIT or event.type == K_ESCAPE:
            pygame.quit()
            exit()

        print(ball.velocity)
        if event.type == MOUSEBUTTONDOWN and ball.is_colliding(pygame.mouse.get_pos()) and ball.velocity.x <= 0.01 and ball.velocity.y <= 0.05:
            vec_move_start = vector(pygame.mouse.get_pos())
            drawing_arrow = True
        if event.type == MOUSEBUTTONUP:
            vec_move_end = vector(pygame.mouse.get_pos())
            drawing_arrow = False   
        
    ball.update()
    
    if vec_move_start != vector(-1,-1) and vec_move_end != vector(-1,-1) and not pygame.mouse.get_pressed()[0]:
        opa = vec_move_end - vec_move_start
        opa.x = abs(opa.x)
        opa.y = abs(opa.y)
        ball.make_move(vec_move_start - vec_move_end, opa//10)
        vec_move_start = (-1,-1)
        vec_move_end = (-1,-1)

    lado_superior = pygame.draw.rect(screen, (255, 0, 255), (0, 0, 800, 10))
    lado_esquerdo = pygame.draw.rect(screen, (255, 0, 255), (0, 0, 10, 600))
    lado_direito = pygame.draw.rect(screen, (255, 0, 255), (400, 300, 10, 200))
    lado_inferior = pygame.draw.rect(screen, (255, 0, 255), (0, 590, 800, 10))
    circulo = pygame.draw.circle(screen, (255, 255, 255), ball.position, ball.ball_radius)
    
    if lado_direito.colliderect(circulo):
        ball.swap_move_x()
    if lado_esquerdo.colliderect(circulo):
        ball.swap_move_x()
    if lado_inferior.colliderect(circulo):
        ball.swap_move_y()
    if lado_superior.colliderect(circulo):
        ball.swap_move_y()

    if drawing_arrow:
        print(-1 * vector(pygame.mouse.get_pos()) + ball.position)
        draw_arrow(screen, (176,196,222), ball.position, -1 * vector(pygame.mouse.get_pos()) + 2 * ball.position)
    pygame.display.flip()    
    

