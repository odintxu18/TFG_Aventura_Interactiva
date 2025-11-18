import pygame

from src.minijuegos.tres_en_raya.application.uses_cases_tres_raya import PlayTurnUseCase
from src.minijuegos.tres_en_raya.domain.board import Tablero
from src.minijuegos.tres_en_raya.infraestructure.infraestructure_tres import get_ia_service


def jugar_tres_en_raya(screen):
    pygame.font.init()
    font = pygame.font.Font(None, 74)
    dificultad = 3  # ejemplo
    ia_service = get_ia_service(dificultad)
    tablero = Tablero()
    use_case = PlayTurnUseCase(tablero, ia_service)

    jugando = True

    while jugando:
        screen.fill((200, 200, 180))

        # Dibujar cuadrícula
        for i in range(3):
            for j in range(3):
                x, y = 150 + j*100, 150 + i*100
                rect = pygame.Rect(x, y, 90, 90)
                pygame.draw.rect(screen, (0,0,0), rect, 2)
                val = tablero.celdas[i*3+j]
                if val:
                    text = font.render(val, True, (0,0,0))
                    screen.blit(text, (x+25, y+10))

        pygame.display.flip()

        if use_case.turno == "X":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    jugando = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    for i in range(3):
                        for j in range(3):
                            rect = pygame.Rect(150 + j*100, 150 + i*100, 90, 90)
                            if rect.collidepoint(mx, my):
                                use_case.jugar_turno(i*3+j)
        else:
            pygame.time.wait(400)
            use_case.jugar_turno()

        if use_case.ganador or tablero.lleno():
            jugando = False
        pygame.time.wait(100)

    return use_case.ganador
