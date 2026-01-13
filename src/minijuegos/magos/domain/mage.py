class Mago:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.max_vida = 20
        self.vida = 20

        # Flags para habilidades de un solo uso
        self.ha_usado_escudo = False
        self.ha_usado_curacion = False

    def recibir_daño(self, cantidad: int):
        self.vida -= cantidad
        if self.vida < 0: self.vida = 0

    def curar(self, cantidad: int):
        self.vida += cantidad
        if self.vida > self.max_vida: self.vida = self.max_vida

    def esta_vivo(self):
        return self.vida > 0