import pygame

def jugar_tres_en_raya(screen):
    font = pygame.font.Font(None, 74)
    tablero = [None] * 9
    turno = "X"
    ganador = None
    jugando = True

    def check_win():
        combos = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a,b,c in combos:
            if tablero[a] == tablero[b] == tablero[c] and tablero[a]:
                return tablero[a]
        return None

    while jugando:
        screen.fill((200, 200, 180))
        for i in range(3):
            for j in range(3):
                x, y = 150 + j*100, 150 + i*100
                rect = pygame.Rect(x, y, 90, 90)
                pygame.draw.rect(screen, (0,0,0), rect, 2)
                val = tablero[i*3+j]
                if val:
                    text = font.render(val, True, (0,0,0))
                    screen.blit(text, (x+25, y+10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jugando = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for i in range(3):
                    for j in range(3):
                        rect = pygame.Rect(150 + j*100, 150 + i*100, 90, 90)
                        if rect.collidepoint(mx, my) and not tablero[i*3+j]:
                            tablero[i*3+j] = turno
                            ganador = check_win()
                            if ganador or all(tablero):
                                jugando = False
                            turno = "O" if turno == "X" else "X"
        pygame.time.wait(100)
    return ganador
