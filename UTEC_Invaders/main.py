import pygame
import sys
from tema import Tema


class Inicio:
    # Crear método init
    def __init__(self):
        #Inicializar pygame
        pygame.init()

        #Dimensiones de la ventana
        self.ancho = 1500
        self.alto = 800

        #Configurar la pantalla
        self.pantalla = pygame.display.set_mode((self.ancho, self.alto))
        pygame.display.set_caption("UTEC Invaders")
        self.pantalla_rect = self.pantalla.get_rect()

        #Cargar imagenes
        self.fondo_menu = pygame.image.load("fondos/menu.png").convert()

        #Crear el boton para inicar
        self.start_button = pygame.Rect((672, 542), (156, 156))
        self.fuente = pygame.font.SysFont("impact", 45)

    # Método para detectar que el usuario presiona el botón de inicio
    def start(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button:
                        mx, my = pygame.mouse.get_pos()
                        if self.start_button.collidepoint((mx, my)):
                            Tema(self).elegir()

            self.pantalla.blit(self.fondo_menu, self.pantalla_rect)
            pygame.display.flip()


if __name__ == "__main__":
    a = Inicio()
    a.start()
