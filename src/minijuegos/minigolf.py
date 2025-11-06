import pygame, math, random
from rival.rival import get_dificultad

def jugar_minigolf(screen):
    font = pygame.font.Font(None, 40)
    clock = pygame.time.Clock()
    dificultad = get_dificultad()

    hoyo = pygame.Vector2(700, 300)
    pelota_jugador = pygame.Vector2(150, 400)
    pelota_ia = pygame.Vector2(150, 200)

    # errores controlados según dificultad (menos error = mejor IA)
    error_ia = max(80 - dificultad * 10, 10)

    # estados
    turno = "jugador"
    potencia = 0
    cargando = False
    velocidad = pygame.Vector2(0, 0)
    velocidad_ia = pygame.Vector2(0, 0)
    fin_turno_ia = False
    jugando = True

    while jugando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if turno == "jugador":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    cargando = True
                    potencia = 0
                elif event.type == pygame.MOUSEBUTTONUP:
                    cargando = False
                    mouse = pygame.Vector2(pygame.mouse.get_pos())
                    direccion = (mouse - pelota_jugador).normalize()
                    velocidad = direccion * potencia / 3
                    turno = "ia"

        # jugador
        if cargando:
            potencia = min(potencia + 5, 300)
        pelota_jugador += velocidad
        velocidad *= 0.98

        # IA
        if turno == "ia" and not fin_turno_ia:
            pygame.time.wait(700)
            # IA calcula dirección con algo de error
            direccion = (hoyo - pelota_ia).normalize()
            desviacion = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)) * (error_ia / 100)
            direccion += desviacion
            direccion = direccion.normalize()
            potencia_ia = random.randint(120, 280)
            velocidad_ia = direccion * potencia_ia / 3
            fin_turno_ia = True

        pelota_ia += velocidad_ia
        velocidad_ia *= 0.98

        # condiciones de fin de turno
        if fin_turno_ia and velocidad_ia.length() < 0.5:
            turno = "fin"

        # dibujo
        screen.fill((180, 200, 160))
        pygame.draw.circle(screen, (0, 0, 0), hoyo, 15)
        pygame.draw.circle(screen, (255, 255, 255), pelota_jugador, 10)
        pygame.draw.circle(screen, (255, 50, 50), pelota_ia, 10)

        texto_turno = f"Turno: {'Tú' if turno=='jugador' else ('IA' if turno=='ia' else 'Resultado')}"
        t_render = font.render(texto_turno, True, (0,0,0))
        screen.blit(t_render, (50, 50))

        if cargando:
            pygame.draw.rect(screen, (255, 0, 0), (50, 550, potencia, 20))

        pygame.display.flip()
        clock.tick(60)

        if turno == "fin":
            dist_jugador = pelota_jugador.distance_to(hoyo)
            dist_ia = pelota_ia.distance_to(hoyo)
            pygame.time.wait(1000)
            return "X" if dist_jugador < dist_ia else "O"
