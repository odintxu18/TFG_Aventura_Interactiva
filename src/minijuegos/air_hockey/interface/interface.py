import pygame

from src.minijuegos.air_hockey.application.uses_cases import AirHockeyUseCase
from src.minijuegos.air_hockey.domain.game import AirHockeyGame
from src.rival.rival import AirHockeyAI, registrar_derrota


def jugar_air_hockey(screen):
    clock = pygame.time.Clock()

    game = AirHockeyGame(800, 600)
    ai = AirHockeyAI()
    controller = AirHockeyUseCase(game, ai)

    running = True
    result = None

    while running:
        screen.fill((20, 20, 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movimiento jugador humano
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game.p1.move(-1)
        if keys[pygame.K_RIGHT]:
            game.p1.move(1)

        # Update IA + físicas
        controller.update()

        # Dibujar
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

        # Comprobación de puntuación
        if game.score1 >= 5:
            result = "X"  # tú ganas
            running = False
        if game.score2 >= 5:
            result = "O"  # IA gana
            registrar_derrota()
            running = False

    pygame.time.wait(600)
    return result
