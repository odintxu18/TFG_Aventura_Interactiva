
import pygame
from historia.generador import generar_historia
from historia.pergamino import mostrar_texto
from minijuegos.tres_en_raya import jugar_tres_en_raya
from rival.rival import get_dificultad, registrar_derrota

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Historia dinámica - Demo")
font = pygame.font.Font(None, 32)

# 1️⃣ Generar historia
historia = generar_historia("venganza", "Luna", "Kai")

# 2️⃣ Mostrar historia tipo pergamino
mostrar_texto(screen, historia, font)

# 3️⃣ Lanzar minijuego
ganador = jugar_tres_en_raya(screen)

# 4️⃣ Registrar resultado
if ganador == "X":  # jugador gana
    mostrar_texto(screen, "¡Has vencido a tu rival!", font)
else:
    registrar_derrota()
    mostrar_texto(screen, "Tu rival te ha superado... (aprende de ti)", font)

pygame.time.wait(3000)
pygame.quit()
