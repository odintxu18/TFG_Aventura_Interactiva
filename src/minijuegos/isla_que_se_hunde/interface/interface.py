import pygame

from src.minijuegos.isla_que_se_hunde.application.use_cases_isla import SupervivenciaTurnUseCase
from src.minijuegos.isla_que_se_hunde.domain.board import Tablero
from src.minijuegos.isla_que_se_hunde.domain.player import Jugador
from src.minijuegos.isla_que_se_hunde.domain.position import Posicion
from src.minijuegos.isla_que_se_hunde.infraestructure.infraestructure import get_ia_service


def jugar_supervivencia(screen):
    pygame.display.set_caption("Supervivencia 7x7")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    tablero = Tablero()
    jugador = Jugador("Jugador", Posicion(0, 0), "X")
    ia = Jugador("IA", Posicion(6, 6), "O")
    use_case = SupervivenciaTurnUseCase(tablero, jugador, ia, get_ia_service())

    jugando = True
    turno_jugador = True
    ganador = None

    while jugando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif turno_jugador and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: use_case.mover_jugador(-1, 0)
                elif event.key == pygame.K_RIGHT: use_case.mover_jugador(1, 0)
                elif event.key == pygame.K_UP: use_case.mover_jugador(0, -1)
                elif event.key == pygame.K_DOWN: use_case.mover_jugador(0, 1)
                elif event.key == pygame.K_SPACE: pass  # quedarse quieto
                turno_jugador = False

        if not turno_jugador:
            pygame.time.wait(400)
            use_case.turno_ia()
            use_case.hundir_casillas()
            ganador = use_case.verificar_fin()
            turno_jugador = True

        # dibujar tablero
        screen.fill((30, 30, 50))
        for y in range(tablero.alto):
            for x in range(tablero.ancho):
                rect = pygame.Rect(100 + x*50, 100 + y*50, 48, 48)
                color = (100, 200, 100) if tablero.casillas[y][x] else (50, 50, 50)
                pygame.draw.rect(screen, color, rect)
                if jugador.vivo and jugador.posicion.x == x and jugador.posicion.y == y:
                    pygame.draw.circle(screen, (50, 150, 255), rect.center, 18)
                elif ia.vivo and ia.posicion.x == x and ia.posicion.y == y:
                    pygame.draw.circle(screen, (255, 100, 100), rect.center, 18)
        pygame.display.flip()

        clock.tick(30)
        if ganador:
            jugando = False

    pygame.time.wait(1000)
    return ganador
