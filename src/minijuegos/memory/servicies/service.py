import random

class IAMemoriaService:
    def __init__(self):
        self.memoria = {}

    def recordar(self, valor, posicion):
        self.memoria.setdefault(valor, []).append(posicion)

    def buscar_par(self, tablero):
        # Busca si hay pares que recuerda sin revelar
        for valor, posiciones in self.memoria.items():
            disponibles = [p for p in posiciones if not tablero.cartas[p].revelada]
            if len(disponibles) >= 2:
                return disponibles[:2]
        return None

    def elegir_carta(self, tablero):
        opciones = [i for i, c in enumerate(tablero.cartas) if not c.revelada]
        return random.choice(opciones) if opciones else None
