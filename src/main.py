import pygame, random
from historia.generador import generar_historia
from historia.pergamino import mostrar_texto
from rival.rival import  registrar_derrota
from src.minijuegos.air_hockey.interface.play_air_hockey import jugar_air_hockey
from src.minijuegos.carrera_criaturas.interface.interface import iniciar_juego
from src.minijuegos.isla_que_se_hunde.interface.interface import jugar_supervivencia
from src.minijuegos.magos.interface.interface import jugar_duelo
from src.minijuegos.memory.interface.interface import jugar_memoria
from src.minijuegos.tanks.interface.interface import jugar_tanques

from src.minijuegos.tres_en_raya.interface.interface_tres import jugar_tres_en_raya

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Historia dinámica - Demo extendida")
font = pygame.font.Font(None, 32)

# Historia inicial
historia = generar_historia("churros", "noroeste", "descanso", "Metrika", "Dicky")
mostrar_texto(screen, historia, font)

# Tres minijuegos distintos
minijuegos = [jugar_tres_en_raya,jugar_memoria,jugar_duelo,jugar_supervivencia, iniciar_juego, jugar_air_hockey, jugar_tanques]
random.shuffle(minijuegos)
derrotas = 0

for juego in minijuegos:
    mostrar_texto(screen, "¡Un nuevo desafío te espera!", font)
    resultado = juego(screen)
    if resultado == "X":
        mostrar_texto(screen, "¡Has ganado este duelo!", font)
    else:
        registrar_derrota()
        derrotas += 1
        mostrar_texto(screen, "Tu rival te ha vencido... aprende de ti.", font)
    if derrotas >= 3:
        mostrar_texto(screen, "Has perdido tres veces... tu historia termina aquí.", font)
        break

mostrar_texto(screen, "Gracias por jugar.", font)
pygame.time.wait(3000)
pygame.quit()
