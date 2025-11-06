import pygame
import time

def mostrar_texto(screen, texto, fuente, color=(0, 0, 0), velocidad=0.02):
    """Despliega texto lentamente como si fuera un pergamino."""
    lineas = []
    palabra_actual = ""
    for char in texto:
        palabra_actual += char
        if char == "\n":
            lineas.append(palabra_actual)
            palabra_actual = ""
        render = fuente.render(palabra_actual, True, color)
        screen.fill((230, 210, 180))  # color pergamino
        y = 50
        for linea in lineas:
            line_render = fuente.render(linea, True, color)
            screen.blit(line_render, (50, y))
            y += 30
        screen.blit(render, (50, y))
        pygame.display.flip()
        time.sleep(velocidad)
