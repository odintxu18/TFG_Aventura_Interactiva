class Carta:
    def __init__(self, valor):
        self.valor = valor
        self.revelada = False

    def revelar(self):
        self.revelada = True

    def ocultar(self):
        self.revelada = False

    def __repr__(self):
        estado = "↑" if self.revelada else "↓"
        return f"[{self.valor}{estado}]"
