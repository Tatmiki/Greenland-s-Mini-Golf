import pygame
from Phase import *

# Classe principal que suportará os sistemas, grupos de sprites e interações 
# relacionadas ao jogo como um todo (pause, game over, etc.)
class Game:
    # Construtor
    def __init__(self, 
                 phase: Phase,
                 screen: pygame.Surface):
        # Atributos privados
        self.__isPaused = False     # Estado de pausado ou não do jogo
        self.__Fase = phase         # Objeto que carregará a fase e sua aparência
        self.screen = screen

    def win(self, screen: pygame.Surface):
        font = pygame.font.SysFont('comic sans', 40, True, False)
        text = font.render("VOCÊ GANHOU!!!!", True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (600, 350)
        screen.blit(text, textRect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.K_RETURN:
                    pygame.quit()
                    exit()

    def draw(self, screen: pygame.Surface):
        self.__Fase.draw(screen)    
    
    def update(self):
        self.__Fase.update()
        if self.__Fase.winner:
            self.win(self.screen)


