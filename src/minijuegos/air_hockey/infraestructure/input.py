import pygame

from src.minijuegos.air_hockey.application.uses_cases import mover_izquierda, mover_derecha, mover_arriba, mover_abajo



def procesar_input(game):
    keys = pygame.key.get_pressed()

    # Jugador 1 (WASD)
    if keys[pygame.K_a]: mover_izquierda(game.p1)
    if keys[pygame.K_d]: mover_derecha(game.p1)
    if keys[pygame.K_w]: mover_arriba(game.p1)
    if keys[pygame.K_s]: mover_abajo(game.p1)

    # Jugador 2 (flechas)
    if keys[pygame.K_LEFT]: mover_izquierda(game.p2)
    if keys[pygame.K_RIGHT]: mover_derecha(game.p2)
    if keys[pygame.K_UP]: mover_arriba(game.p2)
    if keys[pygame.K_DOWN]: mover_abajo(game.p2)
