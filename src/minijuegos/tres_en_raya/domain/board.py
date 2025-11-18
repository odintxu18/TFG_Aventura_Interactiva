class Tablero:
    def __init__(self):
        self.celdas = [None] * 9

    def esta_libre(self, index):
        return self.celdas[index] is None

    def colocar(self, index, simbolo):
        if self.esta_libre(index):
            self.celdas[index] = simbolo
            return True
        return False

    def hay_ganador(self):
        combos = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        for a,b,c in combos:
            if self.celdas[a] == self.celdas[b] == self.celdas[c] and self.celdas[a]:
                return self.celdas[a]
        return None

    def lleno(self):
        return all(self.celdas)
