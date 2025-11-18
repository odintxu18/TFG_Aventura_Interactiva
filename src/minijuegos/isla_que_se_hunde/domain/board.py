import random

from src.minijuegos.isla_que_se_hunde.domain.position import Posicion


class Tablero:
    def __init__(self, ancho=7, alto=7):
        self.ancho = ancho
        self.alto = alto
        self.casillas = [[True for _ in range(ancho)] for _ in range(alto)]

    def casilla_disponible(self, pos: Posicion):
        return self.casillas[pos.y][pos.x]

    def hundir_casillas(self, cantidad=4, jugadores=None):
        hundidas = []
        for _ in range(cantidad):
            libres = [
                (x, y)
                for y in range(self.alto)
                for x in range(self.ancho)
                if self.casillas[y][x]
            ]
            if not libres:
                break
            x, y = random.choice(libres)
            pos = Posicion(x, y)
            # evitar hundir donde hay jugadores
            if jugadores and any(j.posicion.es_igual(pos) for j in jugadores if j.vivo):
                continue
            self.casillas[y][x] = False
            hundidas.append(pos)
        return hundidas
