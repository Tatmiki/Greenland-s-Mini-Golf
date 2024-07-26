import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configuração da tela
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Detecção de Colisão')

# Definição das cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Criação dos retângulos
central_rect = pygame.Rect(screen_width//2 - 50, screen_height//2 - 50, 100, 100)
player_rect = pygame.Rect(screen_width//2 - 25, screen_height//2 + 200, 50, 50)

# Velocidade do jogador
player_speed = 5

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimentação do jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_rect.y -= player_speed
    if keys[pygame.K_s]:
        player_rect.y += player_speed
    if keys[pygame.K_a]:
        player_rect.x -= player_speed
    if keys[pygame.K_d]:
        player_rect.x += player_speed

    # Detecção de colisão
    if player_rect.colliderect(central_rect):
        # Determinação do lado da colisão
        if player_rect.bottom > central_rect.top and player_rect.top < central_rect.top:
            print("Colisão na parte superior do quadrado central")
        if player_rect.top < central_rect.bottom and player_rect.bottom > central_rect.bottom:
            print("Colisão na parte inferior do quadrado central")
        if player_rect.right > central_rect.left and player_rect.left < central_rect.left:
            print("Colisão na parte esquerda do quadrado central")
        if player_rect.left < central_rect.right and player_rect.right > central_rect.right:
            print("Colisão na parte direita do quadrado central")

        
    # Desenho na tela
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, central_rect)
    pygame.draw.rect(screen, BLACK, player_rect)
    pygame.display.flip()

    pygame.time.Clock().tick(60)

# Encerramento do Pygame
pygame.quit()
sys.exit()
