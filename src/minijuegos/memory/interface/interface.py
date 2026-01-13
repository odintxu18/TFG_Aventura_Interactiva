import pygame
from src.minijuegos.memory.domain.board import TableroMemoria
from src.minijuegos.memory.application.use_cases_memory import PlayMemoryTurnUseCase
from src.rival.ai_adapters import MemoryAIAdapter
from src.utils.visuals import mostrar_resultado_final


def jugar_memoria(screen, rival_service):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 50)
    tablero = TableroMemoria(2, 4)
    ai_adapter = MemoryAIAdapter(rival_service)
    use_case = PlayMemoryTurnUseCase(tablero, ai_adapter)

    # --- VARIABLES PARA MACHINE LEARNING ---
    intentos_jugador = 0
    errores_jugador = 0  # Pares levantados que no coinciden
    inicio_tiempo = pygame.time.get_ticks()

    # ---------------------------------------

    def dibujar_memoria():
        screen.fill((220, 220, 250))
        for i, carta in enumerate(tablero.cartas):
            x = 150 + (i % tablero.columnas) * 120
            y = 100 + (i // tablero.columnas) * 150
            rect = pygame.Rect(x, y, 100, 140)
            color = (255, 255, 255) if not carta.revelada else (100, 200, 250)
            pygame.draw.rect(screen, color, rect)
            if carta.revelada:
                screen.blit(font.render(str(carta.valor), True, (0, 0, 0)), (x + 35, y + 50))
        pygame.display.flip()

    jugando = True
    while jugando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "O"
            elif event.type == pygame.MOUSEBUTTONDOWN and use_case.turno == "X":
                mx, my = event.pos
                for i in range(len(tablero.cartas)):
                    if pygame.Rect(150 + (i % 4) * 120, 100 + (i // 4) * 150, 100, 140).collidepoint(mx, my):
                        use_case.jugador_selecciona(i)

        if use_case.turno == "O" and len(use_case.seleccion) == 0:
            pygame.time.wait(600)
            use_case.turno_ia()

        if len(use_case.seleccion) == 2:
            dibujar_memoria()
            pygame.time.wait(800)

            # --- RECOLECCIÓN DATOS ML (Antes de verificar y cambiar turno) ---
            if use_case.turno == "X":
                intentos_jugador += 1
                idx_a, idx_b = use_case.seleccion
                # Si las cartas son distintas, es un error (fallo de memoria o suerte)
                if tablero.get_valor(idx_a) != tablero.get_valor(idx_b):
                    errores_jugador += 1
            # -----------------------------------------------------------------

            use_case.verificar_par()

        dibujar_memoria()
        clock.tick(30)
        if tablero.todas_reveladas(): jugando = False

    # Determinar ganador
    # Lógica original: gana quien NO tuvo el último turno (o quien limpió la mesa)
    ganador = "O" if use_case.ultimo_turno_ia else "X"
    es_victoria = (ganador == "X")

    # --- CÁLCULO MÉTRICAS ML ---
    duracion_seg = (pygame.time.get_ticks() - inicio_tiempo) / 1000
    if duracion_seg == 0: duracion_seg = 1

    # Tiempo medio por intento
    tiempo_por_intento = duracion_seg / intentos_jugador if intentos_jugador > 0 else 0

    # Agresividad:
    # < 2 segundos por pareja = 1.0 (Muy rápido/Impulsivo)
    # > 5 segundos por pareja = 0.0 (Muy lento/Pensativo)
    agresividad = max(0.0, min(1.0, 1.0 - (tiempo_por_intento - 2.0) / 3.0))

    velocidad = intentos_jugador / duracion_seg

    rival_service.registrar_partida(
        game_type="Memory",
        aggro=agresividad,
        speed=velocidad,
        errores=errores_jugador,
        resultado=ganador
    )
    # ---------------------------

    # CAMBIAR FINAL:
    if not es_victoria:
        # Nota: registrar_partida ya incluye la lógica de registrar_derrota internamente
        mostrar_resultado_final(screen, False)
        return "O"
    else:
        mostrar_resultado_final(screen, True)
        return "X"