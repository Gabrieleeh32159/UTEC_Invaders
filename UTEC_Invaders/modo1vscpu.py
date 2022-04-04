import time
import pygame
import sys
from nave import Nave
from bala import Bala
from alien import Alien
from leaderboard import Leaderboard


class Modo1vscpu:
    # Crear el método init
    def __init__(self, a_game, tema):

        #Colores
        self.negro = (0, 0, 0)
        self.rojo = (255, 0, 0)
        self.blanco = (255, 255, 255)
        self.amarillo = (255, 0, 0)

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

        #Traer la clase Alien
        self.alien = Alien(self, self.tema)

        #Crear el grupo balas usando Sprite
        self.balas = pygame.sprite.Group()

        #Crear el grupo aliens usando Sprite
        self.aliens = pygame.sprite.Group()
        self.crear_alien()

        self.velocidad_alien = 0
        self.velocidad_flota = 20
        self.flota_direccion = 1

        #Cargar el fondo de pantalla
        self.fondo = pygame.image.load("fondos/space.jpg").convert()
        self.fondo_rect = self.fondo.get_rect()

        #Crear un reloj
        self.reloj = pygame.time.Clock()

        #Fuente
        self.fuente = a_game.fuente

    # Crear el metodo para jugar
    def jugar(self):
        #SELECCIONAR LA DIFICULTAD
        fondo_dificultad = pygame.image.load("fondos/dificultad_1vscpu.png")
        fondo_rect = fondo_dificultad.get_rect()

        #Botones
        facil_button = pygame.Rect((195, 190), (295, 555))
        medio_button = pygame.Rect((580, 200), (300, 545))
        dificil_button = pygame.Rect((960, 195), (295, 555))
        ingresado = False

        dificultad = ""
        while not ingresado:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if evento.button:
                        if facil_button.collidepoint(mouse):
                            dificultad = "facil"
                            self.velocidad_alien = 2
                            ingresado = True
                        elif medio_button.collidepoint(mouse):
                            dificultad = "medio"
                            self.velocidad_alien = 4
                            ingresado = True
                        elif dificil_button.collidepoint(mouse):
                            dificultad = "dificil"
                            self.velocidad_alien = 6
                            ingresado = True

            self.pantalla.blit(fondo_dificultad, fondo_rect)
            pygame.display.flip()

        #INGRESAR NOMBRE
        jugador = ""
        completado = False
        while not completado:
            nombre_text = self.fuente.render("Ingresa tu nombre de usuario: " + jugador, True, (0, 255, 0))
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return False
                    elif evento.key == pygame.K_RETURN:
                        completado = True
                    elif evento.key == pygame.K_BACKSPACE:
                        jugador = jugador[:-1]
                    else:
                        jugador += evento.unicode
            self.pantalla.blit(self.fondo, self.fondo_rect)

            self.pantalla.blit(nombre_text, (450, 300))
            pygame.display.flip()

        #JUEGO
        go_to_menu = False
        won = False
        lost = False
        regresar = False

        enemigos_asesinados = 0
        balas_usadas = 0

        tiempo_inicio = time.time()

        while not (go_to_menu or won or lost):
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
                        self.disparar_bala()
                        balas_usadas += 1

                elif evento.type == pygame.KEYUP:
                    if evento.key == pygame.K_RIGHT:
                        self.nave.mover_derecha = False
                    elif evento.key == pygame.K_LEFT:
                        self.nave.mover_izquierda = False
                    elif evento.key == pygame.K_DOWN:
                        self.nave.mover_abajo = False
                    elif evento.key == pygame.K_UP:
                        self.nave.mover_arriba = False

            self.pantalla.blit(self.fondo, self.fondo_rect)
            self.nave.mover()

            self.balas.update()
            self.update_alien()

            for bala in self.balas.copy():
                if bala.rect.bottom <= 0:
                    self.balas.remove(bala)

            for bala in self.balas.sprites():
                bala.__show_bullet__()

            if pygame.sprite.groupcollide(self.aliens, self.balas, True, True):
                enemigos_asesinados += 1

            if pygame.sprite.spritecollide(self.nave, self.aliens, True):
                lost = True

            if len(self.aliens) == 0:
                won = True

            self.aliens.draw(self.pantalla)

            self.nave.load_image()

            pygame.display.flip()
            self.reloj.tick(80)
        #CALCULAR PUNTAJE
        tiempo_usado = time.time() - tiempo_inicio

        score_por_enemigos = (1000/3) * (enemigos_asesinados/40)

        if balas_usadas == 0:
            score_por_balas_usadas = 0
        else:
            score_por_balas_usadas = (1000/3) * ((320000 * (balas_usadas**2))/((balas_usadas**4) + 256000000))

        score_por_tiempo = (1000/3) * ((800 * (tiempo_usado**2))/((tiempo_usado**4) + 160000))

        score = score_por_tiempo + score_por_enemigos + score_por_balas_usadas
        score = round(score, 1)

        Leaderboard(self, "1vscpu", dificultad).guardar_puntaje(jugador, score)

    #PANTALLA DEL FINAL
        gano = self.fuente.render("¡FELICIDADES, HAS GANADO!", True, (0, 255, 0))
        perdio = self.fuente.render("¡QUE LÁSTIMA, HAS PERDIDO!", True, (0, 255, 0))

        again = self.fuente.render("Jugar de nuevo", True, (0, 255, 0))
        ir_menu = self.fuente.render("Ir al menú", True, (0, 255, 0))
        salir = self.fuente.render("Salir", True, (0, 255, 0))
        player = self.fuente.render(jugador, True, (0, 255, 0))
        show_score = self.fuente.render(f"Tu puntaje es:   {score}", True, (0, 255, 0))

        #Botones
        again_button = pygame.Rect((100, 710), (275, 35))
        ir_menu_button = pygame.Rect((680, 710), (185, 35))
        salir_button = pygame.Rect((1300, 710), (85, 35))

        nave1_grande = pygame.transform.scale(self.nave.image, (158, 142))

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
                self.pantalla.blit(gano, (520, 150))
            elif lost:
                self.pantalla.blit(perdio, (530, 150))

            self.pantalla.blit(salir, (1300, 700))
            self.pantalla.blit(ir_menu, (680, 700))
            self.pantalla.blit(again, (100, 700))

            self.pantalla.blit(show_score, (600, 250))
            self.pantalla.blit(nave1_grande, (700, 340))
            self.pantalla.blit(player, (700, 510))

            pygame.display.flip()

    # Método que dispara una bala
    def disparar_bala(self):
        nueva_bala = Bala(self, 1)
        self.balas.add(nueva_bala)

    # Método para crear un alien
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
                self._create_flota(numeroAlien, fila)

    # Crear una flota de aliens segun el espacio disponible
    def _create_flota(self, numero_alien, fila):
        alien = Alien(self, self.tema)
        alien_ancho, alien_alto = alien.rect.size
        alien.x = alien_ancho + 2 * alien_ancho * numero_alien
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2*alien.rect.height * fila
        self.aliens.add(alien)

    # Método para actualizar la posición de los aliens en la flota
    def update_alien(self):
        self.aliens.update()
        self.verifica_bordes_flota()

    # Verificia si la flota choca con algun borde de la pantalla
    def verifica_bordes_flota(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.cambiar_direccion()
                break
            if alien.check_vertical_edges():
                self.cambiar_vertical()
                break

    # Cambia la direccion en la que se mueve la flota (horizontal)
    def cambiar_direccion(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.velocidad_flota
        self.flota_direccion *= -1

    # Cambia la direccion en la que se mueve la flota (horizontal)
    def cambiar_vertical(self):
        self.velocidad_flota *= -1
