import pygame
import random


class Paddle:
    def __init__(self, x, y, width=80, height=15, speed=6, color=(200, 200, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.color = color
        # Límites de movimiento vertical (se definirán al iniciar)
        self.min_y = 0
        self.max_y = 0

    @property
    def x(self):
        return self.rect.centerx

    def set_constraints(self, min_y, max_y):
        """Define en qué zona puede moverse la paleta."""
        self.min_y = min_y
        self.max_y = max_y

    def move(self, direction):
        # Movimiento horizontal (X)
        self.rect.x += direction * self.speed
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))

    def move_vertical(self, direction):
        # Movimiento vertical (Y) respetando la mitad del campo
        new_y = self.rect.y + direction * self.speed
        # Clamp (restringir) entre min_y y max_y
        self.rect.y = max(self.min_y, min(new_y, self.max_y - self.rect.height))

    def draw(self, screen):
        # Dibujar paleta con un borde para que se vea mejor
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=10)


class Puck:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 4 * random.choice([-1, 1])  # Saque aleatorio
        self.vy = 4 * random.choice([-1, 1])
        self.radius = 12
        self.max_speed = 9  # Evitar que se vuelva loca

    def update(self, p1, p2):
        self.x += self.vx
        self.y += self.vy

        # --- REBOTE PAREDES (Con un poco de azar) ---
        if self.x <= 0 + self.radius:
            self.x = self.radius
            self.vx *= -1
            self.vy += random.uniform(-1, 1)  # Rebote imperfecto

        elif self.x >= 800 - self.radius:
            self.x = 800 - self.radius
            self.vx *= -1
            self.vy += random.uniform(-1, 1)

        # --- REBOTE PALETAS ---
        # Usamos collidepoint con el centro del puck para simplificar
        hit_p1 = p1.rect.collidepoint(self.x, self.y + self.radius)
        hit_p2 = p2.rect.collidepoint(self.x, self.y - self.radius)

        if hit_p1 or hit_p2:
            self.vy *= -1  # Invertir dirección vertical

            # Acelerar un poco el juego con cada golpe (tensión)
            self.vx *= 1.05
            self.vy *= 1.05

            # Añadir efecto "efecto" (spin) aleatorio al eje X
            self.vx += random.uniform(-2, 2)

            # Controlar velocidad máxima
            if abs(self.vx) > self.max_speed: self.vx = self.max_speed * (1 if self.vx > 0 else -1)
            if abs(self.vy) > self.max_speed: self.vy = self.max_speed * (1 if self.vy > 0 else -1)

            # Evitar que se quede pegado dentro de la paleta (corrección de posición)
            if hit_p1: self.y = p1.rect.top - self.radius - 2
            if hit_p2: self.y = p2.rect.bottom + self.radius + 2

    def draw(self, s):
        pygame.draw.circle(s, (255, 50, 50), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(s, (200, 0, 0), (int(self.x), int(self.y)), self.radius, 2)


class AirHockeyGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # P1 (Abajo)
        self.p1 = Paddle(width // 2 - 40, height - 60, color=(0, 255, 255))  # Cyan
        self.p1.set_constraints(height // 2, height)  # Solo mitad inferior

        # P2 (Arriba - IA)
        self.p2 = Paddle(width // 2 - 40, 40, color=(255, 0, 255))  # Magenta
        self.p2.set_constraints(0, height // 2)  # Solo mitad superior

        self.puck = Puck(width // 2, height // 2)
        self.score1 = 0
        self.score2 = 0

    def update(self):
        self.puck.update(self.p1, self.p2)

        # Goles
        if self.puck.y < 0:
            self.score1 += 1
            self.reset_puck()
        if self.puck.y > self.height:
            self.score2 += 1
            self.reset_puck()

    def reset_puck(self):
        self.puck = Puck(self.width // 2, self.height // 2)
        pygame.time.wait(500)  # Pequeña pausa tras gol

    def draw_board(self, screen):
        # 1. Fondo
        screen.fill((30, 30, 50))

        # 2. Línea central
        pygame.draw.line(screen, (100, 100, 150), (0, self.height // 2), (self.width, self.height // 2), 4)

        # 3. Círculo central
        pygame.draw.circle(screen, (100, 100, 150), (self.width // 2, self.height // 2), 70, 4)
        pygame.draw.circle(screen, (100, 100, 150), (self.width // 2, self.height // 2), 10)

        # 4. Porterías (zonas visuales)
        pygame.draw.rect(screen, (50, 50, 80), (self.width // 2 - 100, 0, 200, 20))
        pygame.draw.rect(screen, (50, 50, 80), (self.width // 2 - 100, self.height - 20, 200, 20))

    def draw(self, screen):
        self.draw_board(screen)
        self.p1.draw(screen)
        self.p2.draw(screen)
        self.puck.draw(screen)

        font = pygame.font.SysFont(None, 60)
        score = font.render(f"{self.score1} - {self.score2}", True, (255, 255, 255))
        screen.blit(score, (self.width // 2 - score.get_width() // 2, self.height // 2 - 20))