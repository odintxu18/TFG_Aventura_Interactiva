import pygame
import math

def jugar_minigolf(screen):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 48)
    pelota = pygame.Vector2(100, 300)
    hoyo = pygame.Vector2(700, 300)
    velocidad = pygame.Vector2(0, 0)
    potencia = 0
    cargando = False
    jugando = True
    ganador = None

    while jugando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jugando = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cargando = True
                potencia = 0
            elif event.type == pygame.MOUSEBUTTONUP:
                cargando = False
                mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
                direccion = (mouse_pos - pelota).normalize()
                velocidad = direccion * potencia / 3

        if cargando:
            potencia = min(potencia + 5, 300)

        pelota += velocidad
        velocidad *= 0.98  # fricción

        # límites
        if pelota.x < 0 or pelota.x > 800:
            velocidad.x *= -1
        if pelota.y < 0 or pelota.y > 600:
            velocidad.y *= -1

        # comprobar si entra al hoyo
        if pelota.distance_to(hoyo) < 20:
            ganador = "X"  # jugador gana
            jugando = False

        # dibujar
        screen.fill((180, 200, 160))
        pygame.draw.circle(screen, (0, 0, 0), hoyo, 20)
        pygame.draw.circle(screen, (255, 255, 255), pelota, 10)
        if cargando:
            pygame.draw.rect(screen, (255, 0, 0), (50, 550, potencia, 20))
        pygame.display.flip()
        clock.tick(60)

    return ganador
