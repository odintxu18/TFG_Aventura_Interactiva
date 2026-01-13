import pygame
from src.minijuegos.magos.application.use_case_mage import DueloMagosUseCase
from src.minijuegos.magos.domain.battle import BatallaElementos
from src.minijuegos.magos.domain.mage import Mago
from src.minijuegos.magos.domain.spell import Elemento, HECHIZOS_DISPONIBLES
from src.rival.ai_adapters import MagosAIAdapter
from src.utils.visuals import mostrar_resultado_final


def dibujar_barra_vida(screen, x, y, vida, max_vida, color):
    # Fondo gris (vida perdida)
    pygame.draw.rect(screen, (50, 50, 50), (x, y, 200, 30))
    # Vida actual
    ancho_vida = int((vida / max_vida) * 200)
    if ancho_vida > 0:
        pygame.draw.rect(screen, color, (x, y, ancho_vida, 30))
    # Borde
    pygame.draw.rect(screen, (255, 255, 255), (x, y, 200, 30), 2)


def jugar_duelo(screen, rival_service):
    font = pygame.font.Font(None, 36)
    # font_grande = pygame.font.Font(None, 60) # No se usa, pero no molesta
    clock = pygame.time.Clock()

    player = Mago("Tú")
    ia = Mago("Rival")
    batalla = BatallaElementos(player, ia)

    ai_adapter = MagosAIAdapter(rival_service)
    duelo = DueloMagosUseCase(ai_adapter)

    # Definir botones
    botones = [
        {"elem": Elemento.FUEGO, "rect": pygame.Rect(150, 500, 120, 60)},
        {"elem": Elemento.AGUA, "rect": pygame.Rect(290, 500, 120, 60)},
        {"elem": Elemento.PLANTA, "rect": pygame.Rect(430, 500, 120, 60)},
        {"elem": Elemento.ESCUDO, "rect": pygame.Rect(600, 500, 100, 60)},
        {"elem": Elemento.CURACION, "rect": pygame.Rect(720, 500, 100, 60)},
    ]

    jugando = True
    mensaje_central = "¡Elige tu hechizo!"

    ia_ultimo_hechizo = None
    jugador_ultimo_hechizo = None

    # --- DATOS PARA MACHINE LEARNING ---
    stats = {
        "ataques": 0,  # Fuego, Agua, Planta
        "defensas": 0,  # Escudo, Curación
        "clicks_totales": 0,
        "inicio_tiempo": pygame.time.get_ticks()
    }

    while jugando:
        screen.fill((30, 20, 40))  # Fondo oscuro mágico

        # --- DIBUJAR ESTADO ---
        # Barras de vida
        dibujar_barra_vida(screen, 100, 100, player.vida, 20, (0, 255, 0))
        screen.blit(font.render(f"Tú: {player.vida}/20", True, (255, 255, 255)), (100, 70))

        dibujar_barra_vida(screen, 500, 100, ia.vida, 20, (255, 50, 50))
        screen.blit(font.render(f"Rival: {ia.vida}/20", True, (255, 255, 255)), (500, 70))

        # Visualización del último choque (Centro)
        if ia_ultimo_hechizo and jugador_ultimo_hechizo:
            # Dibujar lo que tiró el jugador
            color_j = HECHIZOS_DISPONIBLES[jugador_ultimo_hechizo].color
            pygame.draw.circle(screen, color_j, (300, 300), 50)
            text_j = font.render(jugador_ultimo_hechizo[0], True, (0, 0, 0))  # Primera letra
            screen.blit(text_j, (290, 290))

            screen.blit(font.render("VS", True, (255, 255, 255)), (380, 290))

            # Dibujar lo que tiró la IA
            color_ia = HECHIZOS_DISPONIBLES[ia_ultimo_hechizo].color
            pygame.draw.circle(screen, color_ia, (500, 300), 50)
            text_ia = font.render(ia_ultimo_hechizo[0], True, (0, 0, 0))
            screen.blit(text_ia, (490, 290))

        # Mensaje central
        txt_msg = font.render(mensaje_central, True, (255, 255, 100))
        screen.blit(txt_msg, (400 - txt_msg.get_width() // 2, 400))

        # --- BOTONES ---
        for btn in botones:
            elem = btn["elem"]
            color = HECHIZOS_DISPONIBLES[elem].color

            # Verificar si está deshabilitado
            deshabilitado = False
            if elem == Elemento.ESCUDO and player.ha_usado_escudo: deshabilitado = True
            if elem == Elemento.CURACION and player.ha_usado_curacion: deshabilitado = True

            if deshabilitado:
                pygame.draw.rect(screen, (50, 50, 50), btn["rect"])  # Gris oscuro
                pygame.draw.rect(screen, (100, 100, 100), btn["rect"], 2)
            else:
                pygame.draw.rect(screen, color, btn["rect"], border_radius=8)
                pygame.draw.rect(screen, (255, 255, 255), btn["rect"], 2, border_radius=8)

            lbl = font.render(elem, True, (0, 0, 0) if not deshabilitado else (150, 150, 150))
            screen.blit(lbl, (btn["rect"].x + 10, btn["rect"].y + 20))

        pygame.display.flip()

        # --- EVENTOS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "O"

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for btn in botones:
                    elem = btn["elem"]
                    # Chequeo de lógica antes de permitir click
                    if btn["rect"].collidepoint(mx, my):
                        if elem == Elemento.ESCUDO and player.ha_usado_escudo: continue
                        if elem == Elemento.CURACION and player.ha_usado_curacion: continue

                        # --- ML: REGISTRAR INTENCIÓN ---
                        stats["clicks_totales"] += 1
                        if elem in [Elemento.FUEGO, Elemento.AGUA, Elemento.PLANTA]:
                            stats["ataques"] += 1
                        else:
                            stats["defensas"] += 1
                        # -------------------------------

                        # TURNO
                        logs, ia_move = duelo.ejecutar_turno(batalla, elem)

                        # Actualizar estado visual
                        ia_ultimo_hechizo = ia_move
                        jugador_ultimo_hechizo = elem
                        mensaje_central = logs[0] if logs else "..."

                        # Condiciones de victoria / derrota
                        if not player.esta_vivo() or not ia.esta_vivo():

                            # --- ML: CALCULAR PERFIL Y APRENDER ---
                            total_acciones = stats["ataques"] + stats["defensas"]
                            # Si ataca más del 50% de las veces, es agresivo (0.0 a 1.0)
                            agresividad = stats["ataques"] / total_acciones if total_acciones > 0 else 0.5

                            duracion_seg = (pygame.time.get_ticks() - stats["inicio_tiempo"]) / 1000
                            velocidad = total_acciones / duracion_seg if duracion_seg > 0 else 0

                            resultado_str = "O" if not player.esta_vivo() else "X"

                            # Enviamos datos al cerebro
                            rival_service.registrar_partida(
                                "Magos",
                                agresividad,
                                velocidad,
                                errores=0,  # En este juego no medimos errores de click
                                resultado=resultado_str
                            )
                            # --------------------------------------

                            if not player.esta_vivo():
                                mostrar_resultado_final(screen, False)  # Derrota
                                return "O"

                            if not ia.esta_vivo():
                                mostrar_resultado_final(screen, True)  # Victoria
                                return "X"

        clock.tick(30)