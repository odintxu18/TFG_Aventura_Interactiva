import pygame
import sys

# Colores
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
COLOR_TEXT = pygame.Color('white')
COLOR_BG = pygame.Color((30, 30, 40))


class InputBox:
    def __init__(self, x, y, w, h, label_text, default_text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = default_text
        self.label_text = label_text

        # --- CORRECCIÓN AQUÍ ---
        # Antes ponía 'text', ahora es 'self.text'
        self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, COLOR_TEXT)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si el usuario hace clic en la caja, activarla
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False  # Enter desactiva
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

                # Re-renderizar texto
                self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, COLOR_TEXT)

    def draw(self, screen):
        # Dibujar etiqueta (Label) encima de la caja
        font = pygame.font.Font(None, 28)
        label = font.render(self.label_text, True, (200, 200, 200))
        screen.blit(label, (self.rect.x, self.rect.y - 25))

        # Dibujar Texto input
        # Añadimos un pequeño margen (+5, +5) para que el texto no toque el borde
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 10))

        # Dibujar Rectángulo
        pygame.draw.rect(screen, self.color, self.rect, 2)


def mostrar_menu_inicio(screen):
    clock = pygame.time.Clock()
    font_title = pygame.font.Font(None, 60)
    font_btn = pygame.font.Font(None, 40)

    # Definimos las cajas de input con valores por defecto
    input_jugador = InputBox(200, 150, 300, 40, "Nombre Jugador", "")
    input_rival = InputBox(600, 150, 300, 40, "Nombre Rival", "")

    input_p1 = InputBox(200, 300, 200, 40, "Palabra 1", "")
    input_p2 = InputBox(450, 300, 200, 40, "Palabra 2", "")
    input_p3 = InputBox(700, 300, 200, 40, "Palabra 3", "")

    input_boxes = [input_jugador, input_rival, input_p1, input_p2, input_p3]

    # Botón Comenzar
    btn_rect = pygame.Rect(screen.get_width() // 2 - 100, 500, 200, 60)

    run = True
    datos_retorno = None

    while run:
        screen.fill(COLOR_BG)

        # Título
        title = font_title.render("CONFIGURACIÓN DE LA AVENTURA", True, (255, 215, 0))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            for box in input_boxes:
                box.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_rect.collidepoint(event.pos):
                    # Recoger datos y salir
                    datos_retorno = {
                        "jugador": input_jugador.text,
                        "rival": input_rival.text,
                        "p1": input_p1.text,
                        "p2": input_p2.text,
                        "p3": input_p3.text
                    }
                    run = False

        # Dibujar cajas
        for box in input_boxes:
            box.draw(screen)

        # Dibujar Botón
        mouse_pos = pygame.mouse.get_pos()
        # Efecto Hover (cambia de color si pasas el ratón)
        color_btn = (50, 200, 50) if btn_rect.collidepoint(mouse_pos) else (30, 150, 30)

        pygame.draw.rect(screen, color_btn, btn_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), btn_rect, 2, border_radius=10)

        txt_btn = font_btn.render("COMENZAR", True, (255, 255, 255))
        screen.blit(txt_btn,
                    (btn_rect.centerx - txt_btn.get_width() // 2, btn_rect.centery - txt_btn.get_height() // 2))

        pygame.display.flip()
        clock.tick(30)

    return datos_retorno