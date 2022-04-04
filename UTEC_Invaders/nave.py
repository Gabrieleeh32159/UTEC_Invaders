import pygame


class Nave:
    def __init__(self, a_game, tema, numero):
        self.screen = a_game.pantalla
        self.screen_rect = a_game.pantalla.get_rect()

        ruta = tema + f"/nave{numero}.png"

        self.image = pygame.image.load(ruta).convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        self.mover_derecha = False
        self.mover_izquierda = False
        self.mover_arriba = False
        self.mover_abajo = False

    def mover(self):
        if self.mover_derecha and self.rect.right < self.screen_rect.right:
            self.rect.x += 6
        elif self.mover_izquierda and self.rect.left > 0:
            self.rect.x -= 6
        if self.mover_arriba and self.rect.top > 0:
            self.rect.y -= 6
        elif self.mover_abajo and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += 6

    def load_image(self):
        self.screen.blit(self.image, self.rect)
