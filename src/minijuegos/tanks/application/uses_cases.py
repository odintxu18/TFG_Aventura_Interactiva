# src/minijuegos/tanques/application/play_tanques.py

from src.minijuegos.tanks.domain.tank import Tanque, Obstaculo

class JuegoTanques:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.tanque1 = Tanque(100, height // 2, (0, 255, 255))
        self.tanque2 = Tanque(width - 140, height // 2, (255, 0, 255))
        self.ganador = None

        # Obstáculos aleatorios
        self.obstaculos = [Obstaculo.generar_aleatorio(width, height) for _ in range(3)]

    def mover_tanque(self, tanque: Tanque, dx: int, dy: int):
        tanque.mover(dx, dy, self.width, self.height, self.obstaculos)

    def disparar_tanque(self, tanque: Tanque, dx: int, dy: int):
        tanque.disparar(dx, dy)

    def actualizar_balas(self):
        for tanque in [self.tanque1, self.tanque2]:
            for bala in tanque.balas:
                if bala.active:
                    bala.mover()
                    # Colisión con obstáculos
                    for obs in self.obstaculos:
                        if (obs.x < bala.x < obs.x + obs.width and
                            obs.y < bala.y < obs.y + obs.height):
                            bala.active = False

                    # Colisión con otro tanque
                    enemigo = self.tanque1 if tanque == self.tanque2 else self.tanque2
                    if (enemigo.x < bala.x < enemigo.x + enemigo.width and
                        enemigo.y < bala.y < enemigo.y + enemigo.height):
                        self.ganador = "Jugador Azul" if tanque == self.tanque2 else "Jugador Rosa"
                        bala.active = False
