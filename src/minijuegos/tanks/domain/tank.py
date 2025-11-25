# src/minijuegos/tanques/domain/tanque.py

import random
import time

class Tanque:
    def __init__(self, x: int, y: int, color: tuple, width: int = 40, height: int = 40, speed: int = 5):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.speed = speed
        self.balas = []
        self.ultimo_disparo = 0  # timestamp del último disparo

    def mover(self, dx: int, dy: int, limite_x: int, limite_y: int, obstaculos: list):
        new_x = max(0, min(self.x + dx, limite_x - self.width))
        new_y = max(0, min(self.y + dy, limite_y - self.height))

        # Verificar colisión con obstáculos
        for obs in obstaculos:
            if (new_x < obs.x + obs.width and new_x + self.width > obs.x and
                new_y < obs.y + obs.height and new_y + self.height > obs.y):
                return

        self.x, self.y = new_x, new_y

    def disparar(self, dx: int, dy: int):
        now = time.time()
        if now - self.ultimo_disparo >= 0.5:  # cooldown de 0.5 segundos
            self.balas.append(Bala(self.x + self.width//2, self.y + self.height//2, dx, dy, self.color))
            self.ultimo_disparo = now


class Bala:
    def __init__(self, x: int, y: int, dx: int, dy: int, color: tuple, speed: int = 7):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.speed = speed
        self.active = True

    def mover(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed


class Obstaculo:
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple = (50, 50, 50)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    @staticmethod
    def generar_aleatorio(width_limit, height_limit, width=60, height=60):
        x = random.randint(0, width_limit - width)
        y = random.randint(0, height_limit - height)
        return Obstaculo(x, y, width, height, color=(0, 255, 0))
