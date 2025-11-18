class Posicion:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def es_igual(self, otra):
        return self.x == otra.x and self.y == otra.y

    def adyacentes(self):
        movimientos = [(-1,0), (1,0), (0,-1), (0,1)]
        return [Posicion(self.x + dx, self.y + dy) for dx, dy in movimientos]

    def dentro_limites(self, max_x, max_y):
        return 0 <= self.x < max_x and 0 <= self.y < max_y

    def __repr__(self):
        return f"({self.x},{self.y})"
