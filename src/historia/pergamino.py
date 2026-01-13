# src/historia/pergamino.py
import pygame


def wrap_text(text, font, max_width):
    """Divide el texto en líneas que quepan en max_width."""
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        # Probamos a añadir la palabra a la línea actual
        test_line = ' '.join(current_line + [word])
        w, h = font.size(test_line)

        # Gestionar saltos de línea explícitos que vengan de la IA
        if '\n' in word:
            subwords = word.split('\n')
            current_line.append(subwords[0])
            lines.append(' '.join(current_line))
            current_line = [subwords[1]]
        elif w < max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]

    lines.append(' '.join(current_line))
    return lines


def stream_text(screen, texto, font, color=(0, 0, 0), pos=(50, 50), line_height=35, char_speed=50):
    screen_width = screen.get_width()
    # Margen derecho de 100px
    max_text_width = screen_width - pos[0] - 100

    # 1. Pre-procesamos el texto para que tenga los saltos de línea correctos
    wrapped_lines = wrap_text(texto, font, max_text_width)

    # Unimos todo en un solo string con \n para procesarlo carácter a carácter
    final_text_block = "\n".join(wrapped_lines)

    clock = pygame.time.Clock()
    rendered_text = ""
    idx = 0

    # Loop de animación
    # Importante: Permitir salir o saltar texto con una tecla
    while idx < len(final_text_block):
        dt = clock.tick(60) / 1000

        # Gestión de eventos para evitar que se cuelgue la ventana
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Saltar animación
                    rendered_text = final_text_block
                    idx = len(final_text_block)

        if idx < len(final_text_block):
            chars_to_add = max(1, int(char_speed * dt * 20))  # Ajustar velocidad
            rendered_text = final_text_block[:idx + chars_to_add]
            idx += chars_to_add

        # --- DIBUJADO ---
        screen.fill((230, 210, 180))  # Fondo pergamino

        x, y = pos
        # Separamos lo que ya tenemos renderizado por líneas
        lines_to_draw = rendered_text.split('\n')

        for line in lines_to_draw:
            surface = font.render(line, True, color)
            screen.blit(surface, (x, y))
            y += line_height

        pygame.display.flip()