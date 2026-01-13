class DueloMagosUseCase:
    def __init__(self, ia_adapter):
        self.ia_adapter = ia_adapter

    def ejecutar_turno(self, batalla, hechizo_jugador):
        # La IA elige su movimiento
        hechizo_ia = self.ia_adapter.elegir_movimiento(batalla.ia, batalla.jugador)

        # Resolver turno
        logs = batalla.resolver_turno(hechizo_jugador, hechizo_ia)

        return logs, hechizo_ia  # Devolvemos qué tiró la IA para pintarlo