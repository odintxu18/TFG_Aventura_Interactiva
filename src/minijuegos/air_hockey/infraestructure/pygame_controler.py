import pygame

def process_input(p1, p2):
    keys = pygame.key.get_pressed()

    # Player 1 (WASD)
    p1.vx = keys[pygame.K_d] - keys[pygame.K_a]
    p1.vy = keys[pygame.K_s] - keys[pygame.K_w]

    # Player 2 (Arrows)
    p2.vx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    p2.vy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
