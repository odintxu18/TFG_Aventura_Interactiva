
import random

from src.minijuegos.carrera_criaturas.domain.entities import Tablero, Jugador


class MovimientoCriatura:
    """Caso de uso para mover una criatura en el tablero."""
    def __init__(self, tablero: Tablero):
        self.tablero = tablero

    def mover(self, jugador: Jugador, pasos: int):
        nueva_pos = jugador.criatura.posicion + pasos
        if nueva_pos >= len(self.tablero.casillas):
            nueva_pos = len(self.tablero.casillas) - 1
        jugador.criatura.posicion = nueva_pos
        casilla = self.tablero.casillas[nueva_pos]
        # efectos de la casilla
        if casilla.tipo == "trampa":
            jugador.criatura.vida -= 20
        elif casilla.tipo == "boost":
            jugador.criatura.boosts += 1
        casilla.ocupada_por = jugador.nombre
        return casilla.tipo, jugador.criatura.posicion

class GenerarTablero:
    """Caso de uso para inicializar casillas con trampas y boosts."""
    def __init__(self, tablero: Tablero):
        self.tablero = tablero

    def generar(self, num_trampas=3, num_boosts=2):
        posiciones = list(range(len(self.tablero.casillas)))
        random.shuffle(posiciones)
        for pos in posiciones[:num_trampas]:
            self.tablero.casillas[pos].tipo = "trampa"
        for pos in posiciones[num_trampas:num_trampas+num_boosts]:
            self.tablero.casillas[pos].tipo = "boost"
