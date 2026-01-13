import pygame
import random
import sys

from src.minijuegos.tanks.interface.interface import jugar_tanques
# --- IMPORTACIONES NUEVAS ---
from src.utils.menu import mostrar_menu_inicio  # <--- IMPORTAR EL MENÚ

# --- IMPORTACIONES DE DOMINIO Y SERVICIOS ---
from src.historia.generador import generar_siguiente_capitulo
from src.rival.infraestructure.sqlite_repository import SQLiteRivalRepository
from src.rival.application.service import RivalService

# --- IMPORTACIONES DE MINIJUEGOS ---
from src.minijuegos.tres_en_raya.interface.interface_tres import jugar_tres_en_raya
from src.minijuegos.memory.interface.interface import jugar_memoria
from src.minijuegos.magos.interface.interface import jugar_duelo
from src.minijuegos.isla_que_se_hunde.interface.interface import jugar_supervivencia
from src.minijuegos.air_hockey.interface.play_air_hockey import jugar_air_hockey



# --- FUNCIONES DE UTILIDAD VISUAL (wrap_text, stream_text, esperar_tecla...) ---
# (MANTÉN ESTAS FUNCIONES IGUAL QUE EN EL CÓDIGO ANTERIOR)
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        if '\n' in word:
            subwords = word.split('\n')
            current_line.append(subwords[0])
            lines.append(' '.join(current_line))
            current_line = [subwords[1]]
        elif font.size(' '.join(current_line + [word]))[0] < max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))
    return lines


def stream_text(screen, texto, font, color=(0, 0, 0), pos=(50, 50), line_height=35, char_speed=50):
    if not texto: return
    max_text_width = screen.get_width() - pos[0] - 100
    wrapped_lines = wrap_text(texto, font, max_text_width)
    final_text_block = "\n".join(wrapped_lines)
    clock = pygame.time.Clock()
    idx = 0

    while idx <= len(final_text_block):
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                idx = len(final_text_block)

        chars_to_add = max(1, int(char_speed * dt * 20))
        current_text = final_text_block[:idx]
        idx += chars_to_add

        screen.fill((230, 210, 180))
        y = pos[1]
        for line in current_text.split('\n'):
            screen.blit(font.render(line, True, color), (pos[0], y))
            y += line_height

        hint = font.render("[ESPACIO] Saltar/Continuar", True, (150, 130, 100))
        screen.blit(hint, (screen.get_width() - 300, screen.get_height() - 50))

        pygame.display.flip()
        if idx > len(final_text_block): break


def esperar_tecla():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
        pygame.time.wait(100)


def obtener_bolsa_minijuegos(rival_service):
    lista = [
        lambda s: jugar_tres_en_raya(s, rival_service),
        lambda s: jugar_memoria(s, rival_service),
        lambda s: jugar_duelo(s, rival_service),
        lambda s: jugar_supervivencia(s, rival_service),
        lambda s: jugar_air_hockey(s, rival_service),
        lambda s: jugar_tanques(s, rival_service),

    ]
    random.shuffle(lista)
    return lista


# --- MAIN LOOP ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Historia Dinámica TFG - Modo Infinito")
    font = pygame.font.SysFont("Arial", 32)

    # 1. SETUP DE IA Y REPOSITORIO
    repo = SQLiteRivalRepository()
    rival_service = RivalService(repo)

    # --- NUEVO: MOSTRAR MENÚ DE INICIO ---
    print("Mostrando menú de configuración...")
    datos_config = mostrar_menu_inicio(screen)

    # Extraemos los datos introducidos por el usuario
    jugador_nombre = datos_config["jugador"]
    rival_nombre = datos_config["rival"]
    p1 = datos_config["p1"]
    p2 = datos_config["p2"]
    p3 = datos_config["p3"]
    # -------------------------------------

    # 2. VARIABLES DE ESTADO DEL MUNDO
    vidas = 3
    capitulo = 1

    contexto_historia = f"La aventura de {jugador_nombre} comienza."
    resultado_anterior = "Inicio"

    # Inicializar bolsa de juegos
    bolsa_juegos = obtener_bolsa_minijuegos(rival_service)

    # 3. BUCLE INFINITO
    while vidas > 0:

        # --- A. GENERAR HISTORIA ---
        screen.fill((20, 20, 30))
        msg_carga = font.render(f"Generando Capítulo {capitulo}...", True, (255, 255, 255))
        screen.blit(msg_carga, (screen.get_width() // 2 - msg_carga.get_width() // 2, screen.get_height() // 2))
        pygame.display.flip()

        # Llamada a Gemma con los NOMBRES Y PALABRAS REALES
        texto_capitulo = generar_siguiente_capitulo(
            contexto_previo=contexto_historia[-400:],
            resultado_anterior=resultado_anterior,
            palabra1=p1, palabra2=p2, palabra3=p3,
            jugador=jugador_nombre,
            rival=rival_nombre,
            n_capitulo=capitulo
        )

        contexto_historia += f"\n[Cap {capitulo}]: {texto_capitulo}"

        # --- B. MOSTRAR NARRATIVA ---
        stream_text(screen, texto_capitulo, font)
        esperar_tecla()

        # --- C. MINIJUEGO ---
        if not bolsa_juegos:
            bolsa_juegos = obtener_bolsa_minijuegos(rival_service)

        juego_actual = bolsa_juegos.pop()

        # Transición épica
        screen.fill((0, 0, 0))
        txt_vs = font.render(f"¡{jugador_nombre} VS {rival_nombre}!", True, (255, 50, 50))
        screen.blit(txt_vs, (screen.get_width() // 2 - txt_vs.get_width() // 2, screen.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

        # EJECUTAR JUEGO
        try:
            resultado_juego = juego_actual(screen)
        except Exception as e:
            print(f"Error en el minijuego: {e}")
            resultado_juego = "X"

        pygame.display.set_mode((1920, 1080))

        # --- D. CONSECUENCIAS ---
        if resultado_juego == "O":
            vidas -= 1
            resultado_anterior = "Derrota"
            color_res = (200, 50, 50)
            txt_res = f"¡DERROTA! Has perdido una vida. (Restantes: {vidas})"
        else:
            resultado_anterior = "Victoria"
            color_res = (50, 200, 50)
            txt_res = "¡VICTORIA! Recuperas el aliento y sigues adelante."

        screen.fill((30, 30, 30))
        lbl = font.render(txt_res, True, color_res)
        screen.blit(lbl, (screen.get_width() // 2 - lbl.get_width() // 2, screen.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

        capitulo += 1

    stream_text(screen,
                f"GAME OVER\n\n{rival_nombre} ha triunfado finalmente sobre {jugador_nombre}.\nTu historia ha terminado en el capítulo {capitulo}.",
                font)
    esperar_tecla()
    pygame.quit()


if __name__ == "__main__":
    main()