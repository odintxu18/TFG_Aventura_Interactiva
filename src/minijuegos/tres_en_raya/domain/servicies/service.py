import random

class IAService:
    def __init__(self, prob_inteligencia):
        self.prob_inteligencia = prob_inteligencia

    def decision_ia(self):
        return random.random() < self.prob_inteligencia

    def elegir_movimiento(self, tablero):
        # Intentar ganar
        for i in range(9):
            if tablero.esta_libre(i):
                tablero.celdas[i] = "O"
                if tablero.hay_ganador() == "O":
                    return
                tablero.celdas[i] = None
        # Intentar bloquear
        for i in range(9):
            if tablero.esta_libre(i):
                tablero.celdas[i] = "X"
                if tablero.hay_ganador() == "X" and self.decision_ia():
                    tablero.celdas[i] = "O"
                    return
                tablero.celdas[i] = None
        # Aleatorio
        libres = [i for i in range(9) if tablero.esta_libre(i)]
        if libres:
            tablero.celdas[random.choice(libres)] = "O"