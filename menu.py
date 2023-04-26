import pygame
import sys
from modo1vscpu import Modo1vscpu
from modo1vs1 import Modo1vs1
from modo2vscpu import Modo2vscpu
from leaderboard import Leaderboard


class Menu:
    # Crear el método init
    def __init__(self, a_game):
        #Pantalla
        self.alto = a_game.alto
        self.ancho = a_game.ancho
        self.pantalla = a_game.pantalla

        #Fuente
        self.fuente = a_game.fuente

        #imagenes
        self.fondo = pygame.image.load("fondos/menu_2.jpg").convert()
        self.fondo_rect = self.fondo.get_rect()

        #botones
        self.go_tema_button = pygame.Rect((615, 425), (175, 35))
        self.salir_button = pygame.Rect((570, 700), (275, 35))
        self.playervscpu_button = pygame.Rect((620, 230), (150, 35))
        self.twovscpu_button = pygame.Rect((620, 285), (155, 35))
        self.pvp_button = pygame.Rect((650, 335), (95, 35))
        self.instrucciones_button = pygame.Rect((575, 610), (265, 35))
        self.leaderboards_button = pygame.Rect((575, 515), (260, 35))

    # Mostrar el menú donde se elige el modo de juego, entre otros
    def menu(self, tema):
        go_to_tema = False
        while not go_to_tema:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sys.exit()

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        go_to_tema = True

                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.go_tema_button.collidepoint(mouse):
                        go_to_tema = True
                    elif self.salir_button.collidepoint(mouse):
                        sys.exit()
                    elif self.playervscpu_button.collidepoint(mouse):
                        volver_a_jugar_1vscpu = True
                        while volver_a_jugar_1vscpu:
                            volver_a_jugar_1vscpu = Modo1vscpu(self, tema).jugar()
                    elif self.twovscpu_button.collidepoint(mouse):
                        volver_a_jugar_2vscpu = True
                        while volver_a_jugar_2vscpu:
                            volver_a_jugar_2vscpu = Modo2vscpu(self, tema).jugar()
                    elif self.pvp_button.collidepoint(mouse):
                        volver_a_jugar_pvp = True
                        while volver_a_jugar_pvp:
                            volver_a_jugar_pvp = Modo1vs1(self, tema).jugar()

                    elif self.leaderboards_button.collidepoint(mouse):
                        volver = False
                        while not volver:
                            elegir_modo_fondo = pygame.image.load("fondos/elegir_modo_leaderboard.png")
                            playervscpu_button = pygame.Rect((320, 240), (345, 480))
                            twovscpu_button = pygame.Rect((790, 230), (340, 495))
                            modo = ""
                            modo_elegido = False
                            while not modo_elegido:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        sys.exit()
                                    elif event.type == pygame.MOUSEBUTTONDOWN:
                                        mouse2 = pygame.mouse.get_pos()
                                        if event.button:
                                            if playervscpu_button.collidepoint(mouse2):
                                                modo = "1vscpu"
                                                modo_elegido = True
                                            elif twovscpu_button.collidepoint(mouse2):
                                                modo = "2vscpu"
                                                modo_elegido = True
                                    self.pantalla.blit(elegir_modo_fondo, (0, 0))
                                pygame.display.flip()

                            fondo_elegir_dificultad = pygame.image.load("fondos/dificultad_1vscpu.png")

                            if modo == "2vscpu":
                                fondo_elegir_dificultad = pygame.image.load("fondos/dificultad_2vscpu.png")

                            #botones
                            leaderboard_facil_button = pygame.Rect((190, 190), (300, 560))
                            leaderboard_medio_button = pygame.Rect((575, 200), (300, 540))
                            leaderboard_dificil_button = pygame.Rect((960, 195), (1260, 550))

                            dificultad = ""
                            dificultad_elegida = False
                            while not dificultad_elegida:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        sys.exit()
                                    elif event.type == pygame.MOUSEBUTTONDOWN:
                                        mouse3 = pygame.mouse.get_pos()
                                        if event.button:
                                            if leaderboard_facil_button.collidepoint(mouse3):
                                                dificultad = "facil"
                                                dificultad_elegida = True
                                            elif leaderboard_medio_button.collidepoint(mouse3):
                                                dificultad = "medio"
                                                dificultad_elegida = True
                                            elif leaderboard_dificil_button.collidepoint(mouse3):
                                                dificultad = "dificil"
                                                dificultad_elegida = True
                                    self.pantalla.blit(fondo_elegir_dificultad, (0, 0))
                                pygame.display.flip()
                            volver = Leaderboard(self, modo, dificultad).mostrar_puntajes()

                    elif self.instrucciones_button.collidepoint(mouse):
                        instrucciones = pygame.image.load("fondos/instrucciones.png")
                        instrucciones_rect = instrucciones.get_rect()

                        ir_al_menu_button = pygame.Rect((630, 755), (245, 35))
                        regresar = False
                        while not regresar:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    sys.exit()
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        regresar = True
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    if event.button:
                                        mouse = pygame.mouse.get_pos()
                                        if ir_al_menu_button.collidepoint(mouse):
                                            regresar = True

                            self.pantalla.blit(instrucciones, instrucciones_rect)
                            pygame.display.flip()

            self.pantalla.blit(self.fondo, self.fondo_rect)
            pygame.display.flip()
