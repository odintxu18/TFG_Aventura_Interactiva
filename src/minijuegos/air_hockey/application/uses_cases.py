def mover_izquierda(paddle):
    paddle.x -= paddle.speed

def mover_derecha(paddle):
    paddle.x += paddle.speed

def mover_arriba(paddle):
    paddle.y -= paddle.speed

def mover_abajo(paddle):
    paddle.y += paddle.speed
class AirHockeyUseCase:
    def __init__(self, game, ai):
        self.game = game
        self.ai = ai

    def update(self):
        # Movimiento IA
        move = self.ai.mover(self.game.p2, self.game.puck)
        self.game.p2.move(move)

        # Actualizar físicas
        self.game.update()
