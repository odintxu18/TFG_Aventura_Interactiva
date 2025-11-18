import random
from src.domain.entities.carta import Carta

class TableroMemoria:
    def __init__(self, filas=2, columnas=4):
        self.filas = filas
        self.columnas = columnas
        num_cartas = filas * columnas
        valores = list(range(num_cartas // 2)) * 2
        random.shuffle(valores)
        self.cartas = [Carta(v) for v in valores]

    def todas_reveladas(self):
        return all(c.revelada for c in self.cartas)

    def revelar(self, index):
        self.cartas[index].revelar()

    def ocultar(self, a, b):
        self.cartas[a].ocultar()
        self.cartas[b].ocultar()

    def get_valor(self, index):
        return self.cartas[index].valor

