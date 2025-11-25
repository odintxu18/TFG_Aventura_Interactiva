# src/minijuegos/tanques/interface/play_tanques.py

import pygame

from src.minijuegos.tanks.application.uses_cases import JuegoTanques


def jugar_tanques(screen):
    clock = pygame.time.Clock()
    width, height = screen.get_size()
    juego = JuegoTanques(width, height)

    jugando = True
    while jugando:
        screen.fill((0, 0, 0))  # fondo negro

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jugando = False

        keys = pygame.key.get_pressed()
        # Movimiento Jugador 1
        if keys[pygame.K_w]: juego.mover_tanque(juego.tanque1, 0, -juego.tanque1.speed)
        if keys[pygame.K_s]: juego.mover_tanque(juego.tanque1, 0, juego.tanque1.speed)
        if keys[pygame.K_a]: juego.mover_tanque(juego.tanque1, -juego.tanque1.speed, 0)
        if keys[pygame.K_d]: juego.mover_tanque(juego.tanque1, juego.tanque1.speed, 0)
        if keys[pygame.K_SPACE]: juego.disparar_tanque(juego.tanque1, 1, 0)

        # Movimiento Jugador 2
        if keys[pygame.K_UP]: juego.mover_tanque(juego.tanque2, 0, -juego.tanque2.speed)
        if keys[pygame.K_DOWN]: juego.mover_tanque(juego.tanque2, 0, juego.tanque2.speed)
        if keys[pygame.K_LEFT]: juego.mover_tanque(juego.tanque2, -juego.tanque2.speed, 0)
        if keys[pygame.K_RIGHT]: juego.mover_tanque(juego.tanque2, juego.tanque2.speed, 0)
        if keys[pygame.K_RETURN]: juego.disparar_tanque(juego.tanque2, -1, 0)

        # Actualizar balas
        juego.actualizar_balas()

        # Dibujar obstáculos
        for obs in juego.obstaculos:
            pygame.draw.rect(screen, obs.color, (obs.x, obs.y, obs.width, obs.height), border_radius=5)

        # Dibujar tanques
        pygame.draw.rect(screen, juego.tanque1.color,
                         (juego.tanque1.x, juego.tanque1.y, juego.tanque1.width, juego.tanque1.height),
                         border_radius=5)
        pygame.draw.rect(screen, juego.tanque2.color,
                         (juego.tanque2.x, juego.tanque2.y, juego.tanque2.width, juego.tanque2.height),
                         border_radius=5)

        # Dibujar balas
        for tanque in [juego.tanque1, juego.tanque2]:
            for bala in tanque.balas:
                if bala.active:
                    pygame.draw.circle(screen, bala.color, (int(bala.x), int(bala.y)), 5)

        # Mostrar ganador
        if juego.ganador:
            font = pygame.font.Font(None, 64)
            text = font.render(f"{juego.ganador} gana!", True, (255, 255, 0))
            screen.blit(text, (width // 2 - 180, height // 2 - 32))
            pygame.display.flip()
            pygame.time.wait(3000)
            break

        pygame.display.flip()
        clock.tick(60)

    return juego.ganador
