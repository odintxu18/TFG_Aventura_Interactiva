import pygame

def stream_text(
    screen,
    texto,
    font,
    color=(0, 0, 0),
    pos=(50, 50),
    line_height=24,
    char_speed=30  # caracteres por segundo
):
    """
    Muestra texto con animación tipo pergamino, sin bloquear el loop.
    Se llama dentro del bucle principal.
    """

    clock = pygame.time.Clock()
    rendered_lines = [""]  # comienza con la primera línea vacía

    idx = 0

    while idx < len(texto):
        dt = clock.tick(60) / 1000  # delta time en segundos
        chars_to_add = max(1, int(char_speed * dt))

        for _ in range(chars_to_add):
            if idx >= len(texto):
                break

            char = texto[idx]
            idx += 1

            if char == "\n":
                rendered_lines.append("")
            else:
                rendered_lines[-1] += char

        # Dibujado
        screen.fill((230, 210, 180))  # pergamino suave

        y = pos[1]
        for linea in rendered_lines:
            rendered = font.render(linea, True, color)
            screen.blit(rendered, (pos[0], y))
            y += line_height

        pygame.display.flip()

    return rendered_lines
