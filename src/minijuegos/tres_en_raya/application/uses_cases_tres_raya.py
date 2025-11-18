from src.domain.entities.tablero import Tablero
from src.domain.entities.jugador import Jugador

class PlayTurnUseCase:
    def __init__(self, tablero: Tablero, ia_service):
        self.tablero = tablero
        self.ia_service = ia_service
        self.turno = "X"
        self.ganador = None

    def jugar_turno(self, index=None):
        if self.ganador:
            return

        if self.turno == "X":
            if index is not None:
                self.tablero.colocar(index, "X")
                self.turno = "O"
        else:
            self.ia_service.elegir_movimiento(self.tablero)
            self.turno = "X"

        self.ganador = self.tablero.hay_ganador()
        if self.ganador or self.tablero.lleno():
            return self.ganador