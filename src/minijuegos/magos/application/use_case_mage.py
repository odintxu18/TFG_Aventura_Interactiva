

class DueloMagosUseCase:
    def __init__(self, ia_service):
        self.ia = ia_service

    def ejecutar_turno(self, batalla, hechizo_jugador):
        hechizo_ia = self.ia.elegir_hechizo(batalla.mago2.energia)
        resultados = batalla.resolver_turno(hechizo_jugador, hechizo_ia)
        return resultados, batalla.mago1, batalla.mago2
