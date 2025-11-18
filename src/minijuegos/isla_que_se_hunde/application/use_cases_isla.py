from src.minijuegos.isla_que_se_hunde.domain.position import Posicion


class SupervivenciaTurnUseCase:
    def __init__(self, tablero, jugador, ia, ia_service):
        self.tablero = tablero
        self.jugador = jugador
        self.ia = ia
        self.ia_service = ia_service
        self.hundidas = []

    def mover_jugador(self, dx, dy):
        nueva = Posicion(self.jugador.posicion.x + dx, self.jugador.posicion.y + dy)
        self.jugador.mover(nueva, self.tablero)

    def turno_ia(self):
        nueva = self.ia_service.decidir_movimiento(self.ia, self.tablero, self.jugador)
        self.ia.mover(nueva, self.tablero)

    def hundir_casillas(self):
        self.hundidas = self.tablero.hundir_casillas(4, jugadores=[self.jugador, self.ia])
        # comprobar si alguien cae
        for j in [self.jugador, self.ia]:
            if not self.tablero.casilla_disponible(j.posicion):
                j.morir()

    def verificar_fin(self):
        if not self.jugador.vivo:
            return "O"
        if not self.ia.vivo:
            return "X"
        return None
