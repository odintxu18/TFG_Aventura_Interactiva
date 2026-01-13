import random

from src.rival.domain.repository import RivalRepository
from src.rival.application.ml_brain import RivalBrain

class RivalService:
    def __init__(self, repository: RivalRepository):
        self.repository = repository
        self.brain = RivalBrain(repository) # Instanciamos el cerebro ML
        self.config_actual = self.brain.obtener_contramedida() # Config inicial

    def recalcular_estrategia(self):
        """Llamar esto al final de cada partida."""
        self.config_actual = self.brain.obtener_contramedida()

    def get_agresividad_ia(self):
        return self.config_actual.get("agresividad_ia", 0.5)

    def debe_fallar(self) -> bool:
        # Usamos la tasa de error calculada por ML
        tasa_error = self.config_actual.get("tasa_error_ia", 0.2)
        return random.random() < tasa_error

    def registrar_partida(self, game_type, aggro, speed, errores, resultado):
        # 1. Guardar datos crudos
        self.repository.guardar_stats(game_type, aggro, speed, errores, resultado)
        # 2. Registrar derrota simple (para compatibilidad antigua)
        if resultado == "O":
            self.repository.registrar_derrota()
        # 3. APRENDER
        self.recalcular_estrategia()