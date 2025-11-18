class Mago:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.energia = 100
        self.escudo = 0

    def aplicar_daño(self, cantidad: int):
        mitigado = max(0, cantidad - self.escudo)
        self.energia -= mitigado
        self.escudo = 0  # el escudo se gasta
        if self.energia < 0:
            self.energia = 0

    def curar(self, cantidad: int):
        self.energia = min(100, self.energia + cantidad)

    def activar_escudo(self, cantidad: int):
        self.escudo = cantidad

    def esta_vivo(self):
        return self.energia > 0
