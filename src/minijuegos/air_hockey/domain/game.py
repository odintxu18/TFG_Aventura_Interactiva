import pygame

class Paddle:
    def __init__(self, x, y, width=80, height=15, speed=6):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    @property
    def x(self):
        return self.rect.centerx

    def move(self, direction):
        self.rect.x += direction * self.speed
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 255), self.rect)

class Puck:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 5
        self.vy = 5
        self.radius = 10

    def update(self, p1, p2):
        self.x += self.vx
        self.y += self.vy

        # Rebotar paredes
        if self.x <= 0 or self.x >= 800:
            self.vx *= -1

        # Rebotar paletas
        if p1.rect.collidepoint(self.x, self.y):
            self.vy *= -1
        if p2.rect.collidepoint(self.x, self.y):
            self.vy *= -1

    def draw(self, s):
        pygame.draw.circle(s, (255, 100, 100), (self.x, self.y), self.radius)

class AirHockeyGame:
    def __init__(self, width, height):
        self.p1 = Paddle(width // 2, height - 60)
        self.p2 = Paddle(width // 2, 40)
        self.puck = Puck(width // 2, height // 2)
        self.score1 = 0
        self.score2 = 0

    def update(self):
        self.puck.update(self.p1, self.p2)

        # comprobar goles
        if self.puck.y < 0:
            self.score1 += 1
            self.puck = Puck(400, 300)

        if self.puck.y > 600:
            self.score2 += 1
            self.puck = Puck(400, 300)

    def draw(self, screen):
        self.p1.draw(screen)
        self.p2.draw(screen)
        self.puck.draw(screen)

        font = pygame.font.SysFont(None, 40)
        score = font.render(f"{self.score1} - {self.score2}", True, (255, 255, 255))
        screen.blit(score, (370, 10))
