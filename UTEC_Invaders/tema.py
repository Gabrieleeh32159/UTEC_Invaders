import pygame
import sys
from menu import Menu


class Tema:
    def __init__(self, a_game):

        #pantalla
        self.alto = a_game.alto
        self.ancho = a_game.ancho
        self.pantalla = a_game.pantalla

        #imagen
        self.fondo = pygame.image.load("fondos/temas.png").convert()
        self.fondo_rect = self.fondo.get_rect()

        self.juego = a_game
        self.fuente = a_game.fuente

        #botones
        self.boton_star_wars = pygame.Rect((550, 420), (400, 100))
        self.boton_star_trek = pygame.Rect((550, 560), (430, 70))
        self.boton_space_invaders = pygame.Rect((520, 655), (420, 115))
        self.boton_salir_1 = pygame.Rect((15, 735), (285, 40))
        self.boton_salir_2 = pygame.Rect((1185, 735), (285, 40))

    def elegir(self):
        go_to_menu = False
        while not go_to_menu:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        go_to_menu = True
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button:
                        mx, my = pygame.mouse.get_pos()
                        if self.boton_salir_1.collidepoint((mx, my)):
                            sys.exit()
                        elif self.boton_salir_2.collidepoint((mx, my)):
                            sys.exit()
                        elif self.boton_star_wars.collidepoint((mx, my)):
                            Menu(self.juego).menu("star_wars")
                        elif self.boton_star_trek.collidepoint((mx, my)):
                            Menu(self.juego).menu("star_trek")
                        elif self.boton_space_invaders.collidepoint((mx, my)):
                            Menu(self.juego).menu("space_invaders")

            self.pantalla.blit(self.fondo, self.fondo_rect)
            pygame.display.flip()
