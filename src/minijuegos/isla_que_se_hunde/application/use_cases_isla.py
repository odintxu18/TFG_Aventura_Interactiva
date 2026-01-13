from src.minijuegos.isla_que_se_hunde.domain.position import Posicion


class SupervivenciaTurnUseCase:
    def __init__(self, tablero, jugador, ia, ia_service):
        self.tablero = tablero
        self.jugador = jugador
        self.ia = ia
        self.ia_service = ia_service
        self.hundidas = []

    def mover_jugador(self, dx, dy):
        """Intenta mover al jugador. Si no puede, no hace nada."""
        if not self.jugador.vivo: return

        nueva = Posicion(self.jugador.posicion.x + dx, self.jugador.posicion.y + dy)

        # Verificar colisión con el otro jugador
        if nueva.es_igual(self.ia.posicion):
            return  # No puedes moverte encima del rival

        self.jugador.mover(nueva, self.tablero)

    def turno_ia(self):
        """La IA decide y se mueve."""
        if not self.ia.vivo: return

        # Pasamos el jugador para que la IA sepa dónde está y no choque
        nueva = self.ia_service.decidir_movimiento(self.ia, self.tablero, self.jugador)
        self.ia.mover(nueva, self.tablero)

    def hundir_casillas(self):
        """Hunde casillas aleatorias y mata a quien esté encima."""
        self.hundidas = self.tablero.hundir_casillas(4, jugadores=[self.jugador, self.ia])

        # Verificar si alguien se ha caído porque su suelo desapareció
        for j in [self.jugador, self.ia]:
            if not self.tablero.casilla_disponible(j.posicion):
                j.morir()

    def _tiene_movimientos_validos(self, entidad, rival):
        """Revisa si la entidad tiene al menos 1 casilla libre alrededor."""
        adyacentes = entidad.posicion.adyacentes()
        for pos in adyacentes:
            if (pos.dentro_limites(self.tablero.ancho, self.tablero.alto) and
                    self.tablero.casilla_disponible(pos) and
                    not pos.es_igual(rival.posicion)):
                return True  # Tiene salvación
        return False  # Está atrapado

    def verificar_atrapados(self):
        """Mata a los jugadores que no tengan a dónde moverse."""
        if self.jugador.vivo and not self._tiene_movimientos_validos(self.jugador, self.ia):
            self.jugador.morir()

        if self.ia.vivo and not self._tiene_movimientos_validos(self.ia, self.jugador):
            self.ia.morir()

    def verificar_fin(self):
        """Devuelve el ganador si alguien ha muerto."""
        # Primero revisamos si están atrapados antes de declarar ganador
        self.verificar_atrapados()

        if not self.jugador.vivo and not self.ia.vivo:
            return "E"  # Empate (ambos murieron a la vez)
        if not self.jugador.vivo:
            return "O"  # Gana IA
        if not self.ia.vivo:
            return "X"  # Gana Jugador
        return None