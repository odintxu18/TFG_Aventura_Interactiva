import pygame
from src.minijuegos.air_hockey.domain.game import AirHockeyGame
from src.minijuegos.air_hockey.infraestructure.input import procesar_input



def jugar_air_hockey(screen):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 48)

    game = AirHockeyGame(800, 600)

    jugando = True
    while jugando:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "O"

        procesar_input(game)
        game.update()
        dibujar(screen, game, font)

        if game.is_game_over():
            jugando = False

    return "X" if game.score_p1 > game.score_p2 else "O"
