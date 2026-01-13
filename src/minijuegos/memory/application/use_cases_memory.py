# src/minijuegos/memory/application/use_cases_memory.py

from src.minijuegos.memory.domain.board import TableroMemoria


class PlayMemoryTurnUseCase:
    def __init__(self, tablero: TableroMemoria, ia_adapter):
        self.tablero = tablero
        self.ia = ia_adapter
        self.seleccion = []
        self.turno = "X"  # X = jugador, O = IA
        self.ultimo_turno_ia = False

    def jugador_selecciona(self, index):
        if len(self.seleccion) < 2 and not self.tablero.cartas[index].revelada:
            self.tablero.revelar(index)
            # La IA observa lo que haces
            self.ia.recordar(self.tablero.get_valor(index), index)
            self.seleccion.append(index)

    def turno_ia(self):
        self.ultimo_turno_ia = True
        self.seleccion = []  # Limpiamos selección por seguridad

        # 1. INTENTO DE JUGADA INTELIGENTE (Ya conoce un par)
        par = self.ia.buscar_par(self.tablero)
        if par:
            for p in par:
                self.tablero.revelar(p)
                self.ia.recordar(self.tablero.get_valor(p), p)
            self.seleccion = par
            return  # <--- Termina aquí si encontró par

        # 2. PRIMERA CARTA (Aleatoria)
        # Si no conoce par, levanta una al azar
        carta1 = self.ia.elegir_carta(self.tablero, excluidos=[])

        if carta1 is None: return  # No quedan cartas (seguridad)

        self.tablero.revelar(carta1)
        valor1 = self.tablero.get_valor(carta1)
        self.ia.recordar(valor1, carta1)
        self.seleccion.append(carta1)

        # 3. SEGUNDA CARTA (Inteligente o Aleatoria)
        # ¿Tiene la pareja de la carta1 en memoria?
        match = self.ia.buscar_pareja_en_memoria(valor1, carta1, self.tablero)

        if match is not None and self.ia.debe_jugar_bien():
            carta2 = match
        else:
            # Si no la tiene (o falla a propósito), elige otra al azar
            carta2 = self.ia.elegir_carta(self.tablero, excluidos=[carta1])

        if carta2 is not None:
            self.tablero.revelar(carta2)
            self.ia.recordar(self.tablero.get_valor(carta2), carta2)
            self.seleccion.append(carta2)

    def verificar_par(self):
        if len(self.seleccion) == 2:
            a, b = self.seleccion
            if self.tablero.get_valor(a) != self.tablero.get_valor(b):
                self.tablero.ocultar(a, b)
            else:
                # Si coinciden, limpiamos de la memoria de la IA esas posiciones
                # (aunque la lógica de 'disponibles' ya lo maneja, es bueno limpiar)
                pass

            self.seleccion = []
            self.turno = "O" if self.turno == "X" else "X"