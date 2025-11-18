# src/interfaces/pygame_interface.py
import random

import pygame

from src.minijuegos.carrera_criaturas.application.use_cases_run import GenerarTablero, MovimientoCriatura
from src.minijuegos.carrera_criaturas.domain.entities import Tablero, Jugador, Criatura


def iniciar_juego(screen):
    pygame.display.set_caption("Carrera de Criaturas")
    clock = pygame.time.Clock()
    tablero = Tablero()
    generar = GenerarTablero(tablero)
    generar.generar()

    jugador = Jugador(nombre="Jugador", criatura=Criatura("Dragón"))
    ia = Jugador(nombre="IA", criatura=Criatura("Fénix"))

    movimiento = MovimientoCriatura(tablero)
    jugando = True

    while jugando:
        screen.fill((200, 200, 250))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jugando = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pasos = random.randint(1, 3)
                    movimiento.mover(jugador, pasos)
                    # IA mueve automáticamente
                    pasos_ia = random.randint(1, 3)
                    movimiento.mover(ia, pasos_ia)

        # Dibujar tablero y criaturas
        for idx, casilla in enumerate(tablero.casillas):
            color = (100, 200, 100) if casilla.tipo == "boost" else (200, 100, 100) if casilla.tipo == "trampa" else (
                255, 255, 255)
            rect = pygame.Rect(50 + idx * 30, 300, 28, 28)
            pygame.draw.rect(screen, color, rect)
            if jugador.criatura.posicion == idx:
                pygame.draw.circle(screen, (0, 0, 255), rect.center, 10)
            if ia.criatura.posicion == idx:
                pygame.draw.circle(screen, (255, 0, 0), rect.center, 10)

        pygame.display.flip()
        clock.tick(30)
