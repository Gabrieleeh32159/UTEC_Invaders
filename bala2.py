import pygame
from pygame.sprite import Sprite


class Bala2(Sprite):
    def __init__(self, a_game):
        super().__init__()
        self.screen = a_game.pantalla
        self.color = a_game.color_bala_jugador2
        self.rect = pygame.Rect(0, 0, a_game.ancho_bala, a_game.largo_bala)
        self.rect.midbottom = a_game.nave2.rect.midbottom
        self.juego = a_game
        self.y = float(self.rect.y)

    def update(self):
        self.y += self.juego.velocidad_bala_jugador
        self.rect.y = self.y

    def __show_bullet__(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
