import pygame, random, time
from rival.rival import get_dificultad, decision_ia

def jugar_memoria(screen):
    font = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()
    dificultad = get_dificultad()
    prob_recordar = 0.3 + dificultad * 0.12

    cartas = list(range(1, 5)) * 2
    random.shuffle(cartas)
    reveladas = [False] * 8
    seleccion = []
    memoria_ia = {}
    turno = "X"
    puntos_jugador = puntos_ia = 0
    jugando = True

    while jugando:
        screen.fill((230, 230, 255))
        for i in range(8):
            x = (i % 4) * 180 + 100
            y = (i // 4) * 200 + 100
            rect = pygame.Rect(x, y, 100, 100)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            if reveladas[i] or i in seleccion:
                text = font.render(str(cartas[i]), True, (0, 0, 0))
                screen.blit(text, (x+30, y+20))
            else:
                pygame.draw.rect(screen, (100, 100, 200), rect)

        texto_turno = "Turno: " + ("Tú" if turno == "X" else "Rival IA")
        screen.blit(font_small.render(texto_turno, True, (0,0,0)), (50, 40))
        pygame.display.flip()

        # --- Turno del jugador ---
        if turno == "X":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    idx = (y//200)*4 + (x//180)
                    if 0 <= idx < 8 and not reveladas[idx] and idx not in seleccion:
                        seleccion.append(idx)

        # --- Turno de la IA ---
        elif turno == "O":
            pygame.time.wait(1000)
            posibles = [i for i in range(8) if not reveladas[i]]
            eleccion = []
            # IA busca coincidencias en su memoria
            for valor, posiciones in memoria_ia.items():
                if len(posiciones) == 2 and decision_ia(prob_recordar):
                    eleccion = posiciones
                    break
            # si no tiene coincidencia, elige al azar
            if not eleccion:
                eleccion = random.sample(posibles, 2)
            seleccion = eleccion

        # cuando hay dos seleccionadas
        if len(seleccion) == 2:
            a, b = seleccion
            pygame.display.flip()
            time.sleep(1)

            if cartas[a] == cartas[b]:
                reveladas[a] = reveladas[b] = True
                if turno == "X": puntos_jugador += 1
                else: puntos_ia += 1
            else:
                # la IA recuerda las cartas que vio
                if turno == "O":
                    memoria_ia.setdefault(cartas[a], []).append(a)
                    memoria_ia.setdefault(cartas[b], []).append(b)
                turno = "O" if turno == "X" else "X"
            seleccion = []

        if all(reveladas):
            jugando = False
        clock.tick(30)

    return "X" if puntos_jugador >= puntos_ia else "O"
