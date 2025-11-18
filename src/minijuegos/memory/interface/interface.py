import pygame, time

from src.minijuegos.memory.domain.board import TableroMemoria
from src.minijuegos.memory.infraestructure.infraestructure import get_ia_service
from src.minijuegos.memory.application.use_cases_memory import PlayMemoryTurnUseCase




def jugar_memoria(screen):
    pygame.display.set_caption("Memory Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 50)

    tablero = TableroMemoria(2, 4)
    ia_service = get_ia_service()
    use_case = PlayMemoryTurnUseCase(tablero, ia_service)

    def dibujar():
        screen.fill((220, 220, 250))
        for i, carta in enumerate(tablero.cartas):
            x = 150 + (i % tablero.columnas) * 120
            y = 100 + (i // tablero.columnas) * 150
            rect = pygame.Rect(x, y, 100, 140)
            color = (255, 255, 255) if not carta.revelada else (100, 200, 250)
            pygame.draw.rect(screen, color, rect)
            if carta.revelada:
                text = font.render(str(carta.valor), True, (0, 0, 0))
                screen.blit(text, (x + 35, y + 50))
        pygame.display.flip()

    jugando = True
    while jugando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN and use_case.turno == "X":
                mx, my = event.pos
                for i in range(len(tablero.cartas)):
                    rect = pygame.Rect(150 + (i % tablero.columnas) * 120, 100 + (i // tablero.columnas) * 150, 100, 140)
                    if rect.collidepoint(mx, my):
                        use_case.jugador_selecciona(i)

        if use_case.turno == "O" and len(use_case.seleccion) == 0:
            pygame.time.wait(600)
            use_case.turno_ia()

        if len(use_case.seleccion) == 2:
            dibujar()
            pygame.time.wait(800)
            use_case.verificar_par()

        dibujar()
        clock.tick(30)

        if tablero.todas_reveladas():
            jugando = False

    pygame.time.wait(1000)
    ganador = "O" if use_case.ultimo_turno_ia else "X"
    return ganador
