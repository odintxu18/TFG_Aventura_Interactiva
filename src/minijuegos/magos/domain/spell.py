class Elemento:
    FUEGO = "Fuego"
    AGUA = "Agua"
    PLANTA = "Planta"
    ESCUDO = "Escudo"
    CURACION = "Curación"

class Hechizo:
    def __init__(self, tipo: str, color: tuple):
        self.tipo = tipo
        self.color = color

# Definición visual y lógica
HECHIZOS_DISPONIBLES = {
    Elemento.FUEGO: Hechizo(Elemento.FUEGO, (255, 80, 80)),    # Rojo
    Elemento.AGUA: Hechizo(Elemento.AGUA, (80, 150, 255)),     # Azul
    Elemento.PLANTA: Hechizo(Elemento.PLANTA, (80, 200, 100)), # Verde
    Elemento.ESCUDO: Hechizo(Elemento.ESCUDO, (200, 200, 200)),# Gris
    Elemento.CURACION: Hechizo(Elemento.CURACION, (255, 255, 100)) # Amarillo
}