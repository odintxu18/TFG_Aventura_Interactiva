import pygame
import random

def jugar_memoria(screen):
    font = pygame.font.Font(None, 72)
    clock = pygame.time.Clock()
    cartas = list(range(1, 5)) * 2
    random.shuffle(cartas)
    reveladas = [False]*8
    seleccion = []
    jugando = True
    ganador = None
    pares_encontrados = 0

    while jugando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jugando = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // 200
                fila = y // 200
                idx = fila*4//2 + col//2 if fila < 2 else None
                # cálculo simple de posición
                idx = (y//200)*4 + (x//200)
                if idx < 8 and not reveladas[idx]:
                    seleccion.append(idx)

        # lógica del juego
        if len(seleccion) == 2:
            a, b = seleccion
            if cartas[a] == cartas[b]:
                reveladas[a] = reveladas[b] = True
                pares_encontrados += 1
            pygame.time.wait(500)
            seleccion = []

        if pares_encontrados == 4:
            ganador = "X"
            jugando = False

        # dibujar
        screen.fill((210, 210, 230))
        for i in range(8):
            x = (i % 4) * 200 + 50
            y = (i // 4) * 200 + 50
            rect = pygame.Rect(x, y, 100, 100)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            if reveladas[i] or i in seleccion:
                text = font.render(str(cartas[i]), True, (0, 0, 0))
                screen.blit(text, (x+30, y+20))
            else:
                pygame.draw.rect(screen, (100, 100, 200), rect)
        pygame.display.flip()
        clock.tick(30)

    return ganador
