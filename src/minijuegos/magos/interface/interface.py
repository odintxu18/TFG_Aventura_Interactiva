import pygame

from src.minijuegos.magos.application.use_case_mage import DueloMagosUseCase
from src.minijuegos.magos.domain.battle import Batalla
from src.minijuegos.magos.domain.mage import Mago
from src.minijuegos.magos.domain.spell import HECHIZOS
from src.minijuegos.magos.service.service import IAService


def jugar_duelo(screen):
    font = pygame.font.Font(None, 40)
    clock = pygame.time.Clock()
    player = Mago("Jugador")
    ia = Mago("IA")
    batalla = Batalla(player, ia)
    duelo = DueloMagosUseCase(IAService(0.6))

    jugando = True
    log = []
    while jugando:
        screen.fill((30, 30, 50))

        # Dibujar energía
        pygame.draw.rect(screen, (0,255,0), (100, 100, player.energia*2, 25))
        pygame.draw.rect(screen, (255,0,0), (100, 150, ia.energia*2, 25))

        # Dibujar hechizos
        for i, h in enumerate(HECHIZOS):
            rect = pygame.Rect(100 + i*150, 300, 130, 50)
            pygame.draw.rect(screen, (80,80,150), rect)
            text = font.render(h.nombre, True, (255,255,255))
            screen.blit(text, (rect.x + 10, rect.y + 10))

        # Mostrar log
        y = 400
        for l in log[-3:]:
            screen.blit(font.render(l, True, (255,255,255)), (100, y))
            y += 35

        pygame.display.flip()

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jugando = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, h in enumerate(HECHIZOS):
                    rect = pygame.Rect(100 + i*150, 300, 130, 50)
                    if rect.collidepoint(event.pos):
                        resultados, p, o = duelo.ejecutar_turno(batalla, h)
                        log.extend(resultados)
                        if not p.esta_vivo():
                            log.append("¡Has perdido!")
                            jugando = False
                        elif not o.esta_vivo():
                            log.append("¡Has ganado!")
                            jugando = False

        clock.tick(30)
