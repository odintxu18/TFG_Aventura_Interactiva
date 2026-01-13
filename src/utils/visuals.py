import pygame


def mostrar_resultado_final(screen, gano_jugador):
    """
    Muestra un mensaje grande de victoria o derrota y pausa el juego.
    """
    font_final = pygame.font.Font(None, 100)

    texto = "¡HAS GANADO!" if gano_jugador else "¡HAS PERDIDO!"
    color = (50, 255, 50) if gano_jugador else (255, 50, 50)

    # Capa oscura transparente
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # Sombra del texto
    sombra = font_final.render(texto, True, (0, 0, 0))
    rect_sombra = sombra.get_rect(center=(screen.get_width() // 2 + 4, screen.get_height() // 2 + 4))
    screen.blit(sombra, rect_sombra)

    # Texto principal
    txt = font_final.render(texto, True, color)
    rect = txt.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(txt, rect)

    pygame.display.flip()

    # Pausa de 2.5 segundos para celebrar/lamentar
    pygame.time.wait(2500)