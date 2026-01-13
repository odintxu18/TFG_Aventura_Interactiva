import pygame
from src.minijuegos.tres_en_raya.application.uses_cases_tres_raya import PlayTurnUseCase
from src.minijuegos.tres_en_raya.domain.board import Tablero
from src.rival.ai_adapters import TresEnRayaAIAdapter
from src.utils.visuals import mostrar_resultado_final

def jugar_tres_en_raya(screen, rival_service):
    font = pygame.font.Font(None, 74)
    ai_adapter = TresEnRayaAIAdapter(rival_service)
    tablero = Tablero()
    use_case = PlayTurnUseCase(tablero, ai_adapter) # Asegura que UseCase acepte este adapter

    jugando = True
    while jugando:
        screen.fill((200, 200, 180))
        # Dibujar (tu código de dibujo va aquí, resumido)
        for i in range(3):
            for j in range(3):
                rect = pygame.Rect(150 + j*100, 150 + i*100, 90, 90)
                pygame.draw.rect(screen, (0,0,0), rect, 2)
                val = tablero.celdas[i*3+j]
                if val: screen.blit(font.render(val, True, (0,0,0)), (rect.x+25, rect.y+10))
        pygame.display.flip()

        if use_case.turno == "X":
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return "O"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    for i in range(3):
                        for j in range(3):
                            if pygame.Rect(150 + j*100, 150 + i*100, 90, 90).collidepoint(mx, my):
                                use_case.jugar_turno(i*3+j)
        else:
            pygame.time.wait(400)
            use_case.jugar_turno() # La IA juega

        if use_case.ganador or tablero.lleno():
            jugando = False

    pygame.time.wait(500)
    gano_jugador = (use_case.ganador == "X")

    if use_case.ganador == "O":
        rival_service.registrar_victoria_ia()

    # Añadimos la visualización (incluso si es empate se puede ajustar, aquí asumo X gana)
    if use_case.ganador:
        mostrar_resultado_final(screen, gano_jugador)
    else:
        # Caso Empate (opcional mostrar algo o derrota)
        mostrar_resultado_final(screen, False)

    return use_case.ganador if use_case.ganador else "E"