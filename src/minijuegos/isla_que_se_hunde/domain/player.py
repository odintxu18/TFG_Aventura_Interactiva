from src.minijuegos.isla_que_se_hunde.domain.position import Posicion


class Jugador:
    def __init__(self, nombre: str, posicion: Posicion, simbolo: str):
        self.nombre = nombre
        self.posicion = posicion
        self.simbolo = simbolo
        self.vivo = True

    def mover(self, nueva_posicion: Posicion, tablero):
        if not self.vivo:
            return False
        if nueva_posicion.dentro_limites(tablero.ancho, tablero.alto):
            if tablero.casilla_disponible(nueva_posicion):
                self.posicion = nueva_posicion
                return True
        return False

    def morir(self):
        self.vivo = False
