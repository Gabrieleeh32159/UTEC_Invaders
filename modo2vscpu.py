import time
from leaderboard import Leaderboard
import pygame
import sys
from nave import Nave
from alien import Alien
from bala import Bala


class Modo2vscpu:
    #Crear el método init
    def __init__(self, a_game, tema):

        #Colores
        self.negro = (0, 0, 0)
        self.rojo = (255, 0, 0)
        self.blanco = (255, 255, 255)
        self.amarillo = (255, 255, 0)

        # Dimensiones de la pantalla
        self.pantalla_alto = a_game.alto
        self.pantalla_ancho = a_game.ancho
        self.pantalla = a_game.pantalla

        #Propiedades de la bala del jugador
        self.velocidad_bala_jugador = 10
        self.color_bala_jugador = self.amarillo

        #Propiedades de una bala
        self.ancho_bala = 5
        self.largo_bala = 50

        #Tematica elegida
        self.tema = tema

        #Traer la clase Nave
        self.nave = Nave(self, self.tema, 1)
        self.nave2 = Nave(self, self.tema, 2)

        #Traer la clase Alien
        self.alien = Alien(self, self.tema)

        #Crear el grupo balas usando Sprite
        self.balas = pygame.sprite.Group()
        self.balas2 = pygame.sprite.Group()

        #Crear el grupo aliens usando Sprite
        self.aliens = pygame.sprite.Group()
        self.crear_alien()

        self.velocidad_alien = 0
        self.velocidad_flota = 25
        self.flota_direccion = 1

        #Cargar el fondo de pantalla
        self.fondo = pygame.image.load("fondos/space.jpg").convert()
        self.fondo_rect = self.fondo.get_rect()

        #Crear un reloj
        self.reloj = pygame.time.Clock()

        #Fuente
        self.fuente = a_game.fuente

    #Crear el metodo para jugar
    def jugar(self):
        # SELECCIONAR LA DIFICULTAD
        fondo_dificultad = pygame.image.load("fondos/dificultad_2vscpu.png")
        fondo_rect = fondo_dificultad.get_rect()

        #Botones
        facil_button = pygame.Rect((195, 190), (295, 555))
        medio_button = pygame.Rect((580, 200), (300, 545))
        dificil_button = pygame.Rect((960, 195), (295, 555))
        ingresado = False

        #Elegir dificultad
        dificultad = ""
        while not ingresado:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sys.exit()
                #Click a los botones creados
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if evento.button:
                        if facil_button.collidepoint(mouse):
                            dificultad = "facil"
                            self.velocidad_alien = 3
                            ingresado = True
                        elif medio_button.collidepoint(mouse):
                            dificultad = "medio"
                            self.velocidad_alien = 6
                            ingresado = True
                        elif dificil_button.collidepoint(mouse):
                            dificultad = "dificil"
                            self.velocidad_alien = 9
                            ingresado = True

            self.pantalla.blit(fondo_dificultad, fondo_rect)
            pygame.display.flip()

        #INGRESAR NOMBRES
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

            self.pantalla.blit(self.fondo, self.fondo_rect)

            self.pantalla.blit(nombre_text, (400, 300))

            pygame.display.flip()

        #JUEGO
        go_to_menu = False
        won = False
        lost = False
        player1_alive = True
        player2_alive = True

        regresar = False

        killed_by_p1 = 0
        killed_by_p2 = 0

        bullets_by_p1 = 0
        bullets_by_p2 = 0

        tiempo_inicio = time.time()
        while not (go_to_menu or won or lost) and (player1_alive or player2_alive):
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sys.exit()

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        go_to_menu = True
                        regresar = True
                    elif evento.key == pygame.K_RIGHT:
                        self.nave.mover_derecha = True
                    elif evento.key == pygame.K_LEFT:
                        self.nave.mover_izquierda = True
                    elif evento.key == pygame.K_DOWN:
                        self.nave.mover_abajo = True
                    elif evento.key == pygame.K_UP:
                        self.nave.mover_arriba = True
                    elif evento.key == pygame.K_SPACE:
                        self.disparar_bala(1)
                        bullets_by_p1 += 1

                    if evento.key == pygame.K_d:
                        self.nave2.mover_derecha = True
                    elif evento.key == pygame.K_a:
                        self.nave2.mover_izquierda = True
                    elif evento.key == pygame.K_s:
                        self.nave2.mover_abajo = True
                    elif evento.key == pygame.K_w:
                        self.nave2.mover_arriba = True
                    elif evento.key == pygame.K_q:
                        self.disparar_bala(2)
                        bullets_by_p2 += 1

                elif evento.type == pygame.KEYUP:
                    if evento.key == pygame.K_RIGHT:
                        self.nave.mover_derecha = False
                    elif evento.key == pygame.K_LEFT:
                        self.nave.mover_izquierda = False
                    elif evento.key == pygame.K_DOWN:
                        self.nave.mover_abajo = False
                    elif evento.key == pygame.K_UP:
                        self.nave.mover_arriba = False

                    if evento.key == pygame.K_d:
                        self.nave2.mover_derecha = False
                    elif evento.key == pygame.K_a:
                        self.nave2.mover_izquierda = False
                    elif evento.key == pygame.K_s:
                        self.nave2.mover_abajo = False
                    elif evento.key == pygame.K_w:
                        self.nave2.mover_arriba = False

            self.pantalla.blit(self.fondo, self.fondo_rect)

            ########## JUGADOR 1 ##########
            if player1_alive:
                self.nave.mover()
                self.balas.update()

                for bala in self.balas.copy():
                    if bala.rect.bottom <= 0:
                        self.balas.remove(bala)

                for bala in self.balas.sprites():
                    bala.__show_bullet__()

                self.nave.load_image()

            ########## JUGADOR 2 ##########
            if player2_alive:
                self.nave2.mover()
                self.balas2.update()

                for bala in self.balas2.copy():
                    if bala.rect.bottom <= 0:
                        self.balas.remove(bala)

                for bala in self.balas2.sprites():
                    bala.__show_bullet__()

                self.nave2.load_image()

            ########## ALIENS ##########
            self.update_alien()
            self.aliens.draw(self.pantalla)

            ########## COLISIONES ##########
            if pygame.sprite.groupcollide(self.aliens, self.balas, True, True):
                killed_by_p1 += 1

            if pygame.sprite.groupcollide(self.aliens, self.balas2, True, True):
                killed_by_p2 += 1

            if pygame.sprite.spritecollide(self.nave, self.aliens, False):
                player1_alive = False

            if pygame.sprite.spritecollide(self.nave2, self.aliens, False):
                player2_alive = False

            ########## DETERMINAR SI YA SE HA GANADO O  PERDIDO ##########
            if len(self.aliens) == 0:
                won = True

            if not (player1_alive or player2_alive):
                lost = True

            pygame.display.flip()
            self.reloj.tick(80)

        #PUNTAJES
        tiempo_usado = time.time() - tiempo_inicio

        score_por_tiempo = (1000 / 3) * ((800 * (tiempo_usado ** 2)) / ((tiempo_usado ** 4) + 160000))

        #PARA EL JUGADOR 1
        score_por_enemigos1 = (1000 / 3) * (killed_by_p1 / 40)

        if bullets_by_p1 == 0:
            score_por_balas_usadas1 = 0
        else:
            score_por_balas_usadas1 = (1000 / 3) * ((320000 * (bullets_by_p1 ** 2))/((bullets_by_p1 ** 4) + 256000000))

        score1 = (score_por_tiempo + score_por_enemigos1 + score_por_balas_usadas1) / 2
        score1 = round(score1, 1)

        #PARA EL JUGADOR 2
        score_por_enemigos2 = (1000 / 3) * (killed_by_p2 / 40)

        if bullets_by_p2 == 0:
            score_por_balas_usadas2 = 0
        else:
            score_por_balas_usadas2 = (1000 / 3) * ((320000 * (bullets_by_p2 ** 2))/((bullets_by_p2 ** 4) + 256000000))

        score2 = (score_por_tiempo + score_por_enemigos2 + score_por_balas_usadas2) / 2
        score2 = round(score2, 1)

        score_total = score1 + score2

        #GUARDAR PARTIDA
        Leaderboard(self, "2vscpu", dificultad).guardar_puntaje(jugador1 + " y " + jugador2, score_total)

        #PANTALLA FINAL
        ganaron = self.fuente.render("¡FELICIDADES, HAN GANADO!", True, (0, 255, 0))
        perdieron = self.fuente.render("¡QUE LÁSTIMA, HAN PERDIDO!", True, (0, 255, 0))
        scores_are = self.fuente.render("Los puntajes son: ", True, (0, 255, 0))
        show_scores = self.fuente.render(f"{score2}         |         {score1}", True, (0, 255, 0))
        show_total_score = self.fuente.render(f"El puntaje del equipo es: {score_total}", True, (0, 255, 0))

        player1 = self.fuente.render(jugador1, True, (0, 255, 0))
        player2 = self.fuente.render(jugador2, True, (0, 255, 0))

        again = self.fuente.render("Jugar de nuevo", True, (0, 255, 0))
        ir_menu = self.fuente.render("Ir al menú", True, (0, 255, 0))
        salir = self.fuente.render("Salir", True, (0, 255, 0))

        #Botones
        again_button = pygame.Rect((100, 710), (275, 35))
        ir_menu_button = pygame.Rect((680, 710), (185, 35))
        salir_button = pygame.Rect((1300, 710), (85, 35))

        nave1_grande = pygame.transform.scale(self.nave.image, (158, 142))
        nave2_grande = pygame.transform.scale(self.nave2.image, (158, 142))

        while not regresar:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button:
                        mouse = pygame.mouse.get_pos()
                        if again_button.collidepoint(mouse):
                            return True
                        elif ir_menu_button.collidepoint(mouse):
                            return False
                        elif salir_button.collidepoint(mouse):
                            sys.exit()

            self.pantalla.blit(self.fondo, self.fondo_rect)
            if won:
                self.pantalla.blit(ganaron, (520, 150))
            elif lost:
                self.pantalla.blit(perdieron, (530, 150))

            self.pantalla.blit(scores_are, (600, 220))
            self.pantalla.blit(show_scores, (650, 340))
            self.pantalla.blit(show_total_score, (450, 500))

            self.pantalla.blit(salir, (1300, 700))
            self.pantalla.blit(ir_menu, (680, 700))
            self.pantalla.blit(again, (100, 700))

            self.pantalla.blit(player1, (1158, 480))
            self.pantalla.blit(player2, (210, 480))

            self.pantalla.blit(nave2_grande, (200, 300))
            self.pantalla.blit(nave1_grande, (1148, 300))

            pygame.display.flip()

    #Cada disparo se añade un objeto de clase bala al grupo balas
    def disparar_bala(self, nave):
        if nave == 1:
            nueva_bala = Bala(self, 1)
            self.balas.add(nueva_bala)
        elif nave == 2:
            nueva_bala = Bala(self, 2)
            self.balas2.add(nueva_bala)

    #Para los aliens
    def crear_alien(self):
        alien = self.alien
        alien_ancho, alien_alto = alien.rect.size

        espacio_disponible = self.pantalla_ancho - (2 * alien_ancho)
        numero_aliens = espacio_disponible // (2 * alien_ancho)

        nave_alto = self.nave.rect.height
        espacio_disponible_y = self.pantalla_alto - (2 * alien_alto) - 2*nave_alto
        numero_filas = espacio_disponible_y // (2*alien_alto)

        for fila in range(numero_filas):
            for numeroAlien in range(1, numero_aliens):
                self._create_alien(numeroAlien, fila)

    #Crear un alien en cierta posicion y añadir el objeto de clase Alien al grupo aliens
    def _create_alien(self, numero_alien, fila):
        alien = Alien(self, self.tema)
        alien_ancho, alien_alto = alien.rect.size
        alien.x = alien_ancho + 2 * alien_ancho * numero_alien
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2*alien.rect.height * fila
        self.aliens.add(alien)

    #Mover los aliens
    def update_alien(self):
        self.aliens.update()
        self.verifica_bordes_flota()

    #Verificar si algun alien choca con el borde de la pantalla
    def verifica_bordes_flota(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.cambiar_horizontal()
                break
            if alien.check_vertical_edges():
                self.cambiar_vertical()
                break

    #Invertir la dirección del movimiento horizontal
    def cambiar_horizontal(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.velocidad_flota
        self.flota_direccion *= -1

    #Invertir la dirección del movimiento vertical
    def cambiar_vertical(self):
        self.velocidad_flota *= -1
