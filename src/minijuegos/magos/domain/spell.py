class Hechizo:
    def __init__(self, nombre: str, tipo: str, valor: int):
        self.nombre = nombre
        self.tipo = tipo  # 'ataque', 'curacion', 'escudo', 'riesgo'
        self.valor = valor

# Hechizos base del juego
HECHIZOS = [
    Hechizo("Ataque", "ataque", 25),
    Hechizo("Escudo", "escudo", 15),
    Hechizo("Curación", "curacion", 20),
    Hechizo("Riesgo", "riesgo", 40)
]
