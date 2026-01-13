import pygame
from src.minijuegos.isla_que_se_hunde.application.use_cases_isla import SupervivenciaTurnUseCase
from src.minijuegos.isla_que_se_hunde.domain.board import Tablero
from src.minijuegos.isla_que_se_hunde.domain.player import Jugador
from src.minijuegos.isla_que_se_hunde.domain.position import Posicion
from src.rival.ai_adapters import IslaAIAdapter
from src.utils.visuals import mostrar_resultado_final


def jugar_supervivencia(screen, rival_service):
    pygame.display.set_caption("Supervivencia - ¡No te encierres!")
    clock = pygame.time.Clock()

    # Configuramos entidades
    tablero = Tablero()
    jugador = Jugador("Jugador", Posicion(0, 0), "X")
    ia = Jugador("IA", Posicion(6, 6), "O")

    ai_adapter = IslaAIAdapter(rival_service)
    use_case = SupervivenciaTurnUseCase(tablero, jugador, ia, ai_adapter)

    jugando = True
    turno_jugador = True
    ganador = None

    # --- VARIABLES PARA MACHINE LEARNING ---
    turnos_jugador = 0
    tiempo_pensamiento_acumulado = 0
    inicio_partida = pygame.time.get_ticks()
    inicio_turno_actual = pygame.time.get_ticks()  # Para medir cuánto tarda en cada movimiento
    # ---------------------------------------

    while jugando:
        # 1. Verificar si alguien está atrapado AL INICIO de cada frame
        ganador = use_case.verificar_fin()
        if ganador:
            jugando = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "O"

            # Movimiento del Jugador
            if turno_jugador and event.type == pygame.KEYDOWN:
                movio = False

                # --- ML: REGISTRAR TIEMPO DE REACCIÓN ---
                tiempo_actual = pygame.time.get_ticks()
                tiempo_pensamiento_acumulado += (tiempo_actual - inicio_turno_actual)
                turnos_jugador += 1
                # ----------------------------------------

                if event.key == pygame.K_LEFT:
                    use_case.mover_jugador(-1, 0);
                    movio = True
                elif event.key == pygame.K_RIGHT:
                    use_case.mover_jugador(1, 0);
                    movio = True
                elif event.key == pygame.K_UP:
                    use_case.mover_jugador(0, -1);
                    movio = True
                elif event.key == pygame.K_DOWN:
                    use_case.mover_jugador(0, 1);
                    movio = True
                elif event.key == pygame.K_SPACE:
                    movio = True  # Esperar

                if movio:
                    turno_jugador = False

        # Turno de la IA y Hundimiento
        if not turno_jugador and jugando:
            pygame.time.wait(200)
            use_case.turno_ia()

            # Verificar si la IA se encerró sola
            ganador = use_case.verificar_fin()
            if ganador:
                jugando = False
                continue

            pygame.time.wait(200)
            use_case.hundir_casillas()

            # Preparamos el siguiente turno del jugador
            turno_jugador = True
            inicio_turno_actual = pygame.time.get_ticks()  # Reiniciar cronómetro del turno

        # --- DIBUJADO ---
        screen.fill((30, 30, 50))
        for y in range(tablero.alto):
            for x in range(tablero.ancho):
                if tablero.casillas[y][x]:
                    rect = pygame.Rect(100 + x * 50, 100 + y * 50, 48, 48)
                    pygame.draw.rect(screen, (100, 200, 100), rect)

        if jugador.vivo:
            center = (100 + jugador.posicion.x * 50 + 24, 100 + jugador.posicion.y * 50 + 24)
            pygame.draw.circle(screen, (50, 150, 255), center, 18)

        if ia.vivo:
            center = (100 + ia.posicion.x * 50 + 24, 100 + ia.posicion.y * 50 + 24)
            pygame.draw.circle(screen, (255, 100, 100), center, 18)

        pygame.display.flip()
        clock.tick(30)

    # Fin del juego
    pygame.time.wait(500)

    # --- CÁLCULO DE MÉTRICAS ML ---
    duracion_seg = (pygame.time.get_ticks() - inicio_partida) / 1000
    if duracion_seg == 0: duracion_seg = 1

    # Tiempo medio pensando por turno (ms)
    promedio_pensamiento = tiempo_pensamiento_acumulado / turnos_jugador if turnos_jugador > 0 else 1000

    # Agresividad basada en velocidad de decisión:
    # < 500ms por turno = 1.0 (Muy rápido/Instintivo)
    # > 2000ms por turno = 0.0 (Lento/Calculador)
    agresividad = max(0.0, min(1.0, 1.0 - (promedio_pensamiento - 500) / 1500))

    velocidad = turnos_jugador / duracion_seg

    # Si ganador es 'E' (Empate, ambos mueren), lo tratamos como Derrota para el ML ('O')
    resultado_ml = "X" if ganador == "X" else "O"

    rival_service.registrar_partida(
        game_type="Isla",
        aggro=agresividad,
        speed=velocidad,
        errores=0,
        resultado=resultado_ml
    )
    # ------------------------------

    if ganador == "O" or ganador == "E":
        rival_service.registrar_victoria_ia()
        mostrar_resultado_final(screen, False)
        return "O"
    else:
        mostrar_resultado_final(screen, True)
        return "X"