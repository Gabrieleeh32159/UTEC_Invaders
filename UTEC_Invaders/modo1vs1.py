import pygame
import sys
import time
from nave import Nave
from nave2 import Nave2
from bala import Bala
from bala2 import Bala2


class Modo1vs1:
    def __init__(self, a_game, tema):
        self.pantalla = a_game.pantalla
        self.pantalla_alto = a_game.alto

        self.fondo = pygame.image.load("fondos/space.jpg").convert()
        self.rect = self.fondo.get_rect()

        self.nave = Nave(self, tema, 1)
        self.nave2 = Nave2(self, tema)

        #Propiedades de la bala del jugador
        self.velocidad_bala_jugador = 10
        self.color_bala_jugador = (255, 255, 0)
        self.color_bala_jugador2 = (255, 0, 0)

        #Propiedades de una bala
        self.ancho_bala = 5
        self.largo_bala = 50

        # Crear el grupo balas usando Sprite
        self.balas = pygame.sprite.Group()
        self.balas2 = pygame.sprite.Group()

        # Crear un reloj
        self.reloj = pygame.time.Clock()

        self.fuente = a_game.fuente

    def jugar(self):
        # INGRESAR NOMBRES
        completado = False
        jugador1 = ""
        jugador2 = ""
        user = 1
        jugador = ""

        while not completado:
            nombre_text = self.fuente.render(f"Ingrese el usuario del jugador{user}: " + jugador, True, (0, 255, 0))
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return False
                    elif evento.key == pygame.K_RETURN:
                        user += 1
                        if user == 2:
                            jugador1 = jugador
                            jugador = ""
                        elif user == 3:
                            jugador2 = jugador
                    elif evento.key == pygame.K_BACKSPACE:
                        jugador = jugador[:-1]
                    else:
                        jugador += evento.unicode

            if user == 3:
                completado = True

            self.pantalla.blit(self.fondo, self.rect)

            self.pantalla.blit(nombre_text, (400, 300))

            pygame.display.flip()

        #PANTALLA PARA ELEGIR EL TIEMPO
        fondo_eleccion = pygame.image.load("fondos/tiempos.png")

        #Botones
        quince_segundos_button = pygame.Rect((160, 225), (300, 415))
        treinta_segundos_button = pygame.Rect((600, 225), (310, 430))
        un_minuto_button = pygame.Rect((1030, 225), (310, 470))

        continuar = False
        tiempo = int()
        while not continuar:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sys.exit()

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return False

                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button:
                        mouse = pygame.mouse.get_pos()
                        if quince_segundos_button.collidepoint(mouse):
                            tiempo = 15
                            continuar = True
                        elif treinta_segundos_button.collidepoint(mouse):
                            tiempo = 30
                            continuar = True
                        elif un_minuto_button.collidepoint(mouse):
                            tiempo = 60
                            continuar = True
            self.pantalla.blit(fondo_eleccion, self.rect)
            pygame.display.flip()

        #JUGAR
        score_jugador1 = 0
        score_jugador2 = 0

        t1 = time.time()
        t2 = 0
        while tiempo - t2 > 0:

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sys.exit()

                elif evento.type == pygame.KEYDOWN:

                    if evento.key == pygame.K_RIGHT:
                        self.nave.mover_derecha = True
                    elif evento.key == pygame.K_LEFT:
                        self.nave.mover_izquierda = True
                    elif evento.key == pygame.K_SPACE:
                        self.disparar_bala()

                    if evento.key == pygame.K_d:
                        self.nave2.mover_derecha = True
                    elif evento.key == pygame.K_a:
                        self.nave2.mover_izquierda = True
                    elif evento.key == pygame.K_q:
                        self.disparar_bala2()

                elif evento.type == pygame.KEYUP:
                    if evento.key == pygame.K_RIGHT:
                        self.nave.mover_derecha = False
                    elif evento.key == pygame.K_LEFT:
                        self.nave.mover_izquierda = False
                    if evento.key == pygame.K_d:
                        self.nave2.mover_derecha = False
                    elif evento.key == pygame.K_a:
                        self.nave2.mover_izquierda = False

            self.pantalla.blit(self.fondo, self.rect)

            self.nave.mover()
            self.nave2.mover()

            self.balas.update()
            self.balas2.update()

            for bala2 in self.balas2.copy():
                if bala2.rect.top >= self.pantalla_alto:
                    self.balas2.remove(bala2)

            for bala2 in self.balas2.sprites():
                bala2.__show_bullet__()

            for bala in self.balas.copy():
                if bala.rect.bottom <= 0:
                    self.balas.remove(bala)

            for bala in self.balas.sprites():
                bala.__show_bullet__()

            if pygame.sprite.spritecollide(self.nave, self.balas2, True):
                score_jugador2 += 1
            if pygame.sprite.spritecollide(self.nave2, self.balas, True):
                score_jugador1 += 1

            self.nave.load_image()
            self.nave2.load_image()

            t2 = round((time.time() - t1), 1)
            texto_score1 = self.fuente.render(str(score_jugador1), True, (0, 255, 0))
            texto_score2 = self.fuente.render(str(score_jugador2), True, (0, 255, 0))
            linea_score = self.fuente.render("--", True, (0, 255, 0))
            tiempo_texto = self.fuente.render(str(round((tiempo - t2), 1)), True, (0, 255, 0))

            self.pantalla.blit(tiempo_texto, (10, 10))
            self.pantalla.blit(texto_score2, (1450, 360))
            self.pantalla.blit(linea_score, (1450, 390))
            self.pantalla.blit(texto_score1, (1450, 420))

            pygame.display.flip()
            self.reloj.tick(80)

        #pantalla para decir que gano cierto jugador
        nave1_grande = pygame.transform.scale(self.nave.image, (158, 142))
        nave2_grande = pygame.transform.scale(self.nave2.image, (158, 142))
        nave2_grande = pygame.transform.rotate(nave2_grande, 180)

        fin_partida = self.fuente.render("¡LA PARTIDA HA ACABADO!", True, (0, 255, 0))
        el_puntaje_es = self.fuente.render("Los puntajes son:", True, (0, 255, 0))

        player1 = self.fuente.render(jugador1, True, (0, 255, 0))
        player2 = self.fuente.render(jugador2, True, (0, 255, 0))

        puntajes = self.fuente.render(f"{score_jugador2}         |         {score_jugador1}", True, (0, 255, 0))
        pregunta = self.fuente.render("QUÉ DESEAN HACER AHORA?", True, (0, 255, 0))
        again = self.fuente.render("Volver a jugar", True, (0, 255, 0))
        ir_menu = self.fuente.render("Ir al menú", True, (0, 255, 0))
        salir = self.fuente.render("Salir del juego", True, (0, 255, 0))

        again_button = pygame.Rect((625, 585), (225, 35))
        ir_menu_button = pygame.Rect((660, 640), (185, 35))
        salir_button = pygame.Rect((620, 700), (265, 35))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button:
                        mouse = pygame.mouse.get_pos()
                        if again_button.collidepoint(mouse):
                            return True
                        elif ir_menu_button.collidepoint(mouse):
                            return False
                        elif salir_button.collidepoint(mouse):
                            sys.exit()

            self.pantalla.blit(self.fondo, self.rect)
            self.pantalla.blit(nave2_grande, (200, 300))
            self.pantalla.blit(nave1_grande, (1148, 300))
            self.pantalla.blit(fin_partida, (530, 150))
            self.pantalla.blit(el_puntaje_es, (600, 220))
            self.pantalla.blit(puntajes, (650, 340))
            self.pantalla.blit(pregunta, (525, 500))

            self.pantalla.blit(player1, (1158, 480))
            self.pantalla.blit(player2, (210, 480))

            self.pantalla.blit(again, (625, 570))
            self.pantalla.blit(ir_menu, (660, 630))
            self.pantalla.blit(salir, (620, 690))

            pygame.display.flip()

    def disparar_bala(self):
        nueva_bala = Bala(self, 1)
        self.balas.add(nueva_bala)

    def disparar_bala2(self):
        nueva_bala = Bala2(self)
        self.balas2.add(nueva_bala)
