import pygame, random
from historia.generador import generar_historia
from historia.pergamino import mostrar_texto
from minijuegos.tres_en_raya import jugar_tres_en_raya
from minijuegos.minigolf import jugar_minigolf
from minijuegos.memoria import jugar_memoria
from rival.rival import get_dificultad, registrar_derrota

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Historia dinámica - Demo extendida")
font = pygame.font.Font(None, 32)

# Historia inicial
historia = generar_historia("venganza", "Luna", "Kai")
mostrar_texto(screen, historia, font)

# Tres minijuegos distintos
minijuegos = [jugar_tres_en_raya, jugar_minigolf, jugar_memoria]
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
