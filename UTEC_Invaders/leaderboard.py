import pygame
import json
import sys
from collections import OrderedDict


class Leaderboard:
    # Crear el método init
    def __init__(self, a_game, modo, dificultad):
        pygame.init()
        self.screen = a_game.pantalla

        self.fondo = pygame.image.load("fondos/space.jpg")
        self.rect = self.fondo.get_rect()

        self.fuente = a_game.fuente
        self.modo = modo

        self.filename = "jsons/" + modo + "_" + dificultad + ".json"

    # Método para cargar puntaje
    def cargar_puntajes(self):
        with open(self.filename) as file:
            data = json.load(file)
            matriz = []
            for key in data:
                matriz.append([key, data[key]])
            matriz = sorted(matriz, key=lambda matriz: matriz[1], reverse=True)

        datos = {"Usuario": [x[0] for x in matriz], "Puntaje": [x[1] for x in matriz]}

        lista_strings = []

        for i in range(len(datos["Usuario"])):
            lista_strings.append("{}     -     {}     -     {}".format(i+1, datos["Usuario"][i], datos["Puntaje"][i]))
        return lista_strings

    # Método para mostrar los puntajes en pantalla
    def mostrar_puntajes(self):
        lista_puestos = self.cargar_puntajes()
        lista_renderizados = []

        for string in lista_puestos:
            lista_renderizados.append(self.fuente.render(string, True, (0, 255, 0)))
        orden = self.fuente.render("Puesto  -  Nombre  -  Puntaje", True, (0, 255, 0))

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return True

                self.screen.blit(self.fondo, self.rect)
                self.screen.blit(orden, (400, 50))
                y = 100
                for i in lista_renderizados:
                    if y <= 800:
                        self.screen.blit(i, (400, y))
                        y += 70

                pygame.display.flip()

    # Método para guardar un nuevo par (nombre - puntaje)
    def guardar_puntaje(self, nombre, puntaje):
        new_data = OrderedDict({nombre: puntaje})
        new_data.update(json.load(open(self.filename), object_pairs_hook=OrderedDict))
        json.dump(new_data, open(self.filename, "w"))

        with open(self.filename, 'r') as file:
            dic = json.load(file)

            dic2 = {}

            for key in dic:
                if key == nombre:
                    if dic[nombre] < puntaje:
                        dic2[nombre] = puntaje
                    else:
                        dic2[nombre] = dic[key]
                else:
                    dic2[key] = dic[key]
        with open(self.filename, "w") as file:
            json.dump(dic2, file, indent=4)
