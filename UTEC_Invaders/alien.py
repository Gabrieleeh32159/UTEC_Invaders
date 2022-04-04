import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, a_game, tema):
        super().__init__()
        self.screen = a_game.pantalla

        ruta = tema + "/alien_facil.png"

        self.image = pygame.image.load(ruta).convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.juego = a_game

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.x += (self.juego.velocidad_alien * self.juego.flota_direccion)
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if (self.rect.right >= screen_rect.right) or (self.rect.left <= 0):
            return True

    def check_vertical_edges(self):
        screen_rect = self.screen.get_rect()
        if (self.rect.bottom >= screen_rect.bottom) or (self.rect.top <= 0):
            return True
