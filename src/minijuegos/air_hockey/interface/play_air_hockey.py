import pygame
from src.minijuegos.air_hockey.domain.game import AirHockeyGame
from src.minijuegos.air_hockey.application.uses_cases import AirHockeyUseCase
from src.rival.ai_adapters import AirHockeyAIAdapter
from src.utils.visuals import mostrar_resultado_final


def jugar_air_hockey(screen, rival_service):
    clock = pygame.time.Clock()
    game = AirHockeyGame(800, 600)

    # Inyección del adaptador
    ai_adapter = AirHockeyAIAdapter(rival_service)
    controller = AirHockeyUseCase(game, ai_adapter)

    running = True
    result = None

    # --- VARIABLES PARA MACHINE LEARNING ---
    inicio_tiempo = pygame.time.get_ticks()
    frames_totales = 0
    frames_atacando = 0  # Tiempo que pasas cerca de la línea central
    frames_movimiento = 0  # Tiempo que pasas moviéndote
    # ---------------------------------------

    while running:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "O"

        # --- INPUT JUGADOR HUMANO ---
        keys = pygame.key.get_pressed()
        se_mueve = False

        # Movimiento Lateral
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            game.p1.move(-1)
            se_mueve = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            game.p1.move(1)
            se_mueve = True

        # Movimiento Vertical
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            game.p1.move_vertical(-1)
            se_mueve = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            game.p1.move_vertical(1)
            se_mueve = True

        # --- ML DATA COLLECTION ---
        frames_totales += 1
        if se_mueve:
            frames_movimiento += 1

        # Análisis de Posición (Agresividad)
        # El P1 juega en la parte inferior (Y: 300 a 600).
        # Si su Y < 450, está "adelantado" (atacando/presionando).
        # Si su Y > 450, está "retrasado" (defendiendo la portería).
        if game.p1.rect.centery < 450:
            frames_atacando += 1
        # --------------------------

        # --- UPDATE IA & FÍSICAS ---
        controller.update()

        # --- DIBUJADO ---
        game.draw(screen)

        pygame.display.flip()
        clock.tick(60)

        # Condiciones de Victoria
        if game.score1 >= 5:
            result = "X"
            running = False
        if game.score2 >= 5:
            # Nota: No llamamos a registrar_victoria_ia aqui manualmente
            # porque lo hará registrar_partida abajo
            result = "O"
            running = False

    pygame.time.wait(600)

    # --- CÁLCULO DE MÉTRICAS ML ---
    duracion_seg = (pygame.time.get_ticks() - inicio_tiempo) / 1000
    if duracion_seg == 0: duracion_seg = 1

    # Agresividad: % del tiempo que pasas en zona ofensiva
    agresividad = frames_atacando / frames_totales if frames_totales > 0 else 0.5

    # Velocidad: % de frames que te mueves normalizado por tiempo
    # (Si te mueves el 100% del tiempo, es alta intensidad)
    intensidad_movimiento = frames_movimiento / frames_totales if frames_totales > 0 else 0

    # Enviar datos al cerebro
    rival_service.registrar_partida(
        game_type="AirHockey",
        aggro=agresividad,
        speed=intensidad_movimiento * 10,  # Escalamos un poco para que sea comparable
        errores=0,
        resultado=result
    )
    # ------------------------------

    mostrar_resultado_final(screen, result == "X")
    return result