import random
from src.minijuegos.memory.domain.board import TableroMemoria
from src.minijuegos.magos.domain.spell import Elemento


class BaseAIAdapter:
    def __init__(self, rival_service):
        self.service = rival_service

    @property
    def dificultad(self):
        """Basada en victorias/derrotas (Skill)."""
        return self.service.get_nivel_inteligencia()

    @property
    def agresividad(self):
        """Basada en Machine Learning (Estilo). 0.0 (Defensivo) a 1.0 (Agresivo)."""
        # Si el servicio no tiene el método aun (por versiones), default 0.5
        return getattr(self.service, 'get_agresividad_ia', lambda: 0.5)()

    def debe_jugar_bien(self):
        """Decide si comete un error forzado o juega óptimo."""
        return not self.service.debe_fallar()


# --- 1. AIR HOCKEY ---
class AirHockeyAIAdapter(BaseAIAdapter):
    def mover(self, paddle, puck):
        # Si toca fallar, hace un movimiento aleatorio
        if not self.debe_jugar_bien():
            return random.choice([-1, 0, 1])

        # Lógica Óptima
        # Si es muy agresiva, intenta interceptar antes
        offset = 0
        if self.agresividad > 0.7:
            offset = 10  # Se adelanta un poco

        if puck.x < paddle.x - offset:
            return -1
        elif puck.x > paddle.x + offset:
            return 1
        return 0


# --- 2. TRES EN RAYA ---
class TresEnRayaAIAdapter(BaseAIAdapter):
    def elegir_movimiento(self, tablero):
        # 1. SIEMPRE Intentar ganar (Prioridad máxima)
        for i in range(9):
            if tablero.esta_libre(i):
                tablero.celdas[i] = "O"
                if tablero.hay_ganador() == "O": return
                tablero.celdas[i] = None

        # 2. Bloquear al jugador
        # Si es Agresiva, a veces ignora bloquear para intentar ganar después (riesgo)
        juega_defensivo = self.agresividad < 0.6

        if self.debe_jugar_bien() or juega_defensivo:
            for i in range(9):
                if tablero.esta_libre(i):
                    tablero.celdas[i] = "X"
                    if tablero.hay_ganador() == "X":
                        tablero.celdas[i] = "O";
                        return
                    tablero.celdas[i] = None

        # 3. Movimiento estratégico o Aleatorio
        libres = [i for i in range(9) if tablero.esta_libre(i)]
        if not libres: return

        # Si es defensiva, prefiere el centro (4)
        if juega_defensivo and 4 in libres:
            tablero.celdas[4] = "O"
            return

        tablero.celdas[random.choice(libres)] = "O"


# --- 3. MEMORY ---
class MemoryAIAdapter(BaseAIAdapter):
    def __init__(self, rival_service):
        super().__init__(rival_service)
        self.memoria = {}

    def recordar(self, valor, posicion):
        # La capacidad de recordar depende de la dificultad (skill)
        if self.debe_jugar_bien():
            self.memoria.setdefault(valor, []).append(posicion)

    def buscar_par(self, tablero):
        for valor, posiciones in self.memoria.items():
            disponibles = [p for p in posiciones if not tablero.cartas[p].revelada]
            if len(disponibles) >= 2: return disponibles[:2]
        return None

    def buscar_pareja_en_memoria(self, valor_carta, index_carta, tablero):
        if valor_carta in self.memoria:
            candidatos = [p for p in self.memoria[valor_carta] if p != index_carta and not tablero.cartas[p].revelada]
            if candidatos: return candidatos[0]
        return None

    def elegir_carta(self, tablero, excluidos=[]):
        opciones = [i for i, c in enumerate(tablero.cartas) if not c.revelada and i not in excluidos]
        return random.choice(opciones) if opciones else None


# --- 4. MAGOS (ELEMENTOS + ML) ---
class MagosAIAdapter(BaseAIAdapter):
    def elegir_movimiento(self, mago_ia, mago_jugador):
        estilo = self.agresividad  # 0.0 (Def) a 1.0 (Aggro)

        # 1. Lógica de Supervivencia (Prioridad absoluta si va a morir)
        if not mago_ia.ha_usado_curacion and mago_ia.vida < 6:
            if self.debe_jugar_bien(): return Elemento.CURACION

        # 2. IA DEFENSIVA (Estilo < 0.4)
        if estilo < 0.4:
            # Prioriza protegerse
            if not mago_ia.ha_usado_escudo and random.random() < 0.6:
                return Elemento.ESCUDO
            if not mago_ia.ha_usado_curacion and mago_ia.vida < 15:
                return Elemento.CURACION

        # 3. IA AGRESIVA (Estilo > 0.6)
        if estilo > 0.6:
            # Spamea ataques
            return random.choice([Elemento.FUEGO, Elemento.AGUA, Elemento.PLANTA])

        # 4. Comportamiento Equilibrado / Aleatorio
        # A veces usa escudo random
        if not mago_ia.ha_usado_escudo and random.random() < 0.1:
            return Elemento.ESCUDO

        return random.choice([Elemento.FUEGO, Elemento.AGUA, Elemento.PLANTA])


# --- 5. ISLA ---
class IslaAIAdapter(BaseAIAdapter):
    def decidir_movimiento(self, ia_entity, tablero, jugador_entity):
        opciones = ia_entity.posicion.adyacentes()
        validas = [o for o in opciones if
                   o.dentro_limites(tablero.ancho, tablero.alto) and tablero.casilla_disponible(o) and not o.es_igual(
                       jugador_entity.posicion)]

        if not validas: return ia_entity.posicion

        # Si la IA juega bien, usa lógica. Si falla, random.
        if self.debe_jugar_bien():
            # ESTILO AGRESIVO: Intenta acercarse al jugador para bloquearle
            if self.agresividad > 0.6:
                # Ordenar por distancia al jugador (la menor distancia primero)
                mejor = min(validas,
                            key=lambda p: abs(p.x - jugador_entity.posicion.x) + abs(p.y - jugador_entity.posicion.y))
                return mejor

            # ESTILO DEFENSIVO: Busca el espacio más abierto (con más vecinos libres)
            else:
                mejor = max(validas, key=lambda p: len([adj for adj in p.adyacentes() if
                                                        adj.dentro_limites(tablero.ancho,
                                                                           tablero.alto) and tablero.casilla_disponible(
                                                            adj)]))
                return mejor

        return random.choice(validas)


# --- 6. TANKS ---
class TanksAIAdapter(BaseAIAdapter):
    def actuar(self, tanque_ia, tanque_jugador, juego):
        distancia_x = abs(tanque_ia.x - tanque_jugador.x)

        # ESTILO AGRESIVO: Se acerca mucho
        distancia_seguridad = 50 if self.agresividad > 0.6 else 200

        if self.debe_jugar_bien():
            # Movimiento
            if distancia_x > distancia_seguridad:
                # Acercarse
                dx = -tanque_ia.speed if tanque_ia.x > tanque_jugador.x else tanque_ia.speed
                juego.mover_tanque(tanque_ia, dx, 0)
            elif distancia_x < 40 and self.agresividad < 0.4:
                # Alejarse (si es defensivo y está muy cerca)
                dx = tanque_ia.speed if tanque_ia.x > tanque_jugador.x else -tanque_ia.speed
                juego.mover_tanque(tanque_ia, dx, 0)

            # Disparo (si está alineado en Y o cerca)
            alineados_y = abs(tanque_ia.y - tanque_jugador.y) < 40

            if alineados_y or (self.agresividad > 0.8 and random.random() < 0.1):
                juego.disparar_tanque(tanque_ia, 0, 1)  # Disparo hacia abajo (asumiendo IA es P2)
        else:
            # Movimiento errático
            if random.random() < 0.05: juego.disparar_tanque(tanque_ia, 0, 1)
            if random.random() < 0.1:
                dx = random.choice([-tanque_ia.speed, tanque_ia.speed])
                juego.mover_tanque(tanque_ia, dx, 0)


# --- 7. CARRERA ---
class CarreraAIAdapter(BaseAIAdapter):
    def calcular_pasos(self):
        # En la carrera, "Jugar bien" significa tener suerte con los dados
        if self.debe_jugar_bien():
            # Si es agresivo, "fuerza" más 3s
            weights = [10, 20, 70] if self.agresividad > 0.5 else [10, 40, 50]
            return random.choices([1, 2, 3], weights=weights)[0]
        return random.randint(1, 3)