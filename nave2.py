import pygame


class Nave2:
    def __init__(self, a_game, tema):
        self.screen = a_game.pantalla
        self.screen_rect = a_game.pantalla.get_rect()

        ruta = tema + "/nave2.png"

        self.nave2 = pygame.image.load(ruta).convert()
        self.image = pygame.transform.rotate(self.nave2, 180)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.midtop = self.screen_rect.midtop
        self.rect.y += 50

        self.mover_derecha = False
        self.mover_izquierda = False

    def mover(self):
        if self.mover_derecha and self.rect.right < self.screen_rect.right:
            self.rect.x += 6
        elif self.mover_izquierda and self.rect.left > 0:
            self.rect.x -= 6

    def load_image(self):
        self.screen.blit(self.image, self.rect)
