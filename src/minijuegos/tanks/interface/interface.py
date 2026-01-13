import pygame
from src.minijuegos.tanks.application.uses_cases import JuegoTanques
from src.rival.ai_adapters import TanksAIAdapter
from src.utils.visuals import mostrar_resultado_final


def jugar_tanques(screen, rival_service):
    clock = pygame.time.Clock()
    width, height = screen.get_size()
    juego = JuegoTanques(width, height)
    ai_adapter = TanksAIAdapter(rival_service)

    jugando = True

    # --- VARIABLES PARA MACHINE LEARNING ---
    movimientos_jugador = 0  # Cuantos frames se ha movido
    disparos_jugador = 0  # Cuantos frames ha intentado disparar
    inicio_tiempo = pygame.time.get_ticks()
    # ---------------------------------------

    while jugando:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "O"

        keys = pygame.key.get_pressed()

        # --- RECOLECCIÓN DE DATOS DE JUGADOR 1 ---
        se_mueve = False
        if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
            movimientos_jugador += 1
            se_mueve = True

        if keys[pygame.K_SPACE]:
            disparos_jugador += 1
        # -----------------------------------------

        # Lógica de Movimiento Jugador 1
        if keys[pygame.K_w]: juego.mover_tanque(juego.tanque1, 0, -juego.tanque1.speed)
        if keys[pygame.K_s]: juego.mover_tanque(juego.tanque1, 0, juego.tanque1.speed)
        if keys[pygame.K_a]: juego.mover_tanque(juego.tanque1, -juego.tanque1.speed, 0)
        if keys[pygame.K_d]: juego.mover_tanque(juego.tanque1, juego.tanque1.speed, 0)
        if keys[pygame.K_SPACE]: juego.disparar_tanque(juego.tanque1, 1, 0)

        # Jugador 2 (IA) controlado por Adapter
        ai_adapter.actuar(juego.tanque2, juego.tanque1, juego)

        juego.actualizar_balas()

        # Dibujado
        for obs in juego.obstaculos:
            pygame.draw.rect(screen, obs.color, (obs.x, obs.y, obs.width, obs.height))

        pygame.draw.rect(screen, juego.tanque1.color,
                         (juego.tanque1.x, juego.tanque1.y, juego.tanque1.width, juego.tanque1.height))
        pygame.draw.rect(screen, juego.tanque2.color,
                         (juego.tanque2.x, juego.tanque2.y, juego.tanque2.width, juego.tanque2.height))

        for t in [juego.tanque1, juego.tanque2]:
            for b in t.balas:
                if b.active:
                    pygame.draw.circle(screen, b.color, (int(b.x), int(b.y)), 5)

        pygame.display.flip()
        clock.tick(60)

        if juego.ganador:
            es_victoria = (juego.ganador != "Jugador Azul")  # Azul era la IA

            # --- CÁLCULO DE MÉTRICAS ML ---
            duracion_seg = (pygame.time.get_ticks() - inicio_tiempo) / 1000
            if duracion_seg == 0: duracion_seg = 1

            total_acciones = movimientos_jugador + disparos_jugador

            # Agresividad: Ratio Disparos vs Movimiento.
            # Si solo disparas (1.0), eres muy agresivo. Si solo corres (0.0), defensivo.
            if total_acciones > 0:
                agresividad = disparos_jugador / total_acciones
            else:
                agresividad = 0.5  # Equilibrado por defecto

            # Velocidad: Cuán activo has estado (acciones por segundo)
            # Normalizamos dividiendo por 60 fps (aproximado)
            velocidad = (total_acciones / 60) / duracion_seg

            # Enviar datos al cerebro
            rival_service.registrar_partida(
                game_type="Tanks",
                aggro=agresividad,
                speed=velocidad,
                errores=0,
                resultado="X" if es_victoria else "O"
            )
            # ------------------------------

            if not es_victoria:
                result = "O"
            else:
                result = "X"

            # MOSTRAR MENSAJE
            mostrar_resultado_final(screen, es_victoria)
            return result

    return "O"