from src.minijuegos.tres_en_raya.domain.servicies.service import IAService


def get_ia_service(dificultad: int):
    prob_inteligencia = 0.3 + (dificultad * 0.12)
    return IAService(prob_inteligencia)
