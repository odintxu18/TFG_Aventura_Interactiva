from src.minijuegos.memory.domain.board import TableroMemoria
from src.minijuegos.memory.servicies.service import IAMemoriaService


class PlayMemoryTurnUseCase:
    def __init__(self, tablero: TableroMemoria, ia_service: IAMemoriaService):
        self.tablero = tablero
        self.ia = ia_service
        self.seleccion = []
        self.turno = "X"  # X = jugador, O = IA
        self.ultimo_turno_ia = False

    def jugador_selecciona(self, index):
        if len(self.seleccion) < 2 and not self.tablero.cartas[index].revelada:
            self.tablero.revelar(index)
            self.ia.recordar(self.tablero.get_valor(index), index)
            self.seleccion.append(index)

    def turno_ia(self):
        self.ultimo_turno_ia = True
        par = self.ia.buscar_par(self.tablero)
        if par:
            for p in par:
                self.tablero.revelar(p)
                self.ia.recordar(self.tablero.get_valor(p), p)
            self.seleccion = par
        else:
            elegido = self.ia.elegir_carta(self.tablero)
            if elegido is not None:
                self.tablero.revelar(elegido)
                self.ia.recordar(self.tablero.get_valor(elegido), elegido)
                self.seleccion.append(elegido)

    def verificar_par(self):
        if len(self.seleccion) == 2:
            a, b = self.seleccion
            if self.tablero.get_valor(a) != self.tablero.get_valor(b):
                self.tablero.ocultar(a, b)
            else:
                # si coincide, IA "olvida" esas posiciones
                self.ia.memoria[self.tablero.get_valor(a)] = [
                    p for p in self.ia.memoria[self.tablero.get_valor(a)]
                    if not self.tablero.cartas[p].revelada
                ]
            self.seleccion = []
            self.turno = "O" if self.turno == "X" else "X"
