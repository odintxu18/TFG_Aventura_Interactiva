import random


class IASupervivenciaService:
    def decidir_movimiento(self, ia, tablero, jugador):
        opciones = ia.posicion.adyacentes()
        opciones = [
            o for o in opciones
            if o.dentro_limites(tablero.ancho, tablero.alto)
            and tablero.casilla_disponible(o)
            and not o.es_igual(jugador.posicion)
        ]
        if not opciones:
            return ia.posicion
        # movimiento aleatorio "seguro"
        return random.choice(opciones)
