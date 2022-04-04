import pygame
from pygame.sprite import Sprite


class Bala(Sprite):
    def __init__(self, a_game, tipo):
        super().__init__()
        self.screen = a_game.pantalla
        if tipo == 1:
            self.color = a_game.color_bala_jugador
            self.nave = a_game.nave
        elif tipo == 2:
            self.color = (255, 0, 0)
            self.nave = a_game.nave2
        self.rect = pygame.Rect(0, 0, a_game.ancho_bala, a_game.largo_bala)
        self.rect.midtop = self.nave.rect.midtop
        self.juego = a_game
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.juego.velocidad_bala_jugador
        self.rect.y = self.y

    def __show_bullet__(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
