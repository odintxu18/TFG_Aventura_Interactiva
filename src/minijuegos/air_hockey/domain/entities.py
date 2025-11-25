class Paddle:
    def __init__(self, x, y, radius=28, speed=7):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed


class Puck:
    def __init__(self, x, y, radius=12, vx=5, vy=5):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = vx
        self.vy = vy

