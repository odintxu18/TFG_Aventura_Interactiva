import random

from src.minijuegos.magos.domain.spell import HECHIZOS


class IAService:
    def __init__(self, agresividad: float = 0.5):
        self.agresividad = agresividad  # 0 = defensiva, 1 = agresiva

    def elegir_hechizo(self, energia_actual):
        # Si está débil, probabilidad de curarse
        if energia_actual < 40 and random.random() > self.agresividad:
            return next(h for h in HECHIZOS if h.tipo == "curacion")
        # Si está protegido, tal vez ataque
        if random.random() < self.agresividad:
            return next(h for h in HECHIZOS if h.tipo == "ataque")
        # Ocasionalmente usa riesgo
        if random.random() < 0.2:
            return next(h for h in HECHIZOS if h.tipo == "riesgo")
        # Por defecto, escudo
        return next(h for h in HECHIZOS if h.tipo == "escudo")
