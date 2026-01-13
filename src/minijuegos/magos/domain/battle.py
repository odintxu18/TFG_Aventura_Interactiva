from src.minijuegos.magos.domain.spell import Elemento


class BatallaElementos:
    def __init__(self, jugador, ia):
        self.jugador = jugador
        self.ia = ia
        self.mensaje_resultado = ""

    def resolver_turno(self, hechizo_j, hechizo_ia):
        """
        Devuelve una lista de logs y aplica el daño.
        Reglas:
        - Fuego > Planta > Agua > Fuego (5 daño)
        - Empate elemento (3 daño ambos)
        - Escudo bloquea todo.
        - Curación +7 (o +5 si recibes ataque).
        """
        # Validar usos únicos (por seguridad)
        if hechizo_j == Elemento.ESCUDO: self.jugador.ha_usado_escudo = True
        if hechizo_j == Elemento.CURACION: self.jugador.ha_usado_curacion = True
        if hechizo_ia == Elemento.ESCUDO: self.ia.ha_usado_escudo = True
        if hechizo_ia == Elemento.CURACION: self.ia.ha_usado_curacion = True

        dano_j = 0
        dano_ia = 0
        cura_j = 0
        cura_ia = 0
        log = []

        # --- 1. Calcular Daño Base (sin aplicar escudos ni curas aún) ---

        # Caso EMPATE DE ELEMENTOS (Ambos pierden 3)
        if hechizo_j in [Elemento.FUEGO, Elemento.AGUA, Elemento.PLANTA] and hechizo_j == hechizo_ia:
            dano_j = 3
            dano_ia = 3
            log.append("¡Choque de elementos! Ambos reciben 3 de daño.")

        # Casos de VICTORIA/DERROTA ELEMENTAL
        else:
            # Jugador ataca
            if self._gana(hechizo_j, hechizo_ia):
                dano_ia = 5
                log.append(f"¡{hechizo_j} quema/moja/corta a {hechizo_ia}!")

            # IA ataca
            if self._gana(hechizo_ia, hechizo_j):
                dano_j = 5
                log.append(f"¡{hechizo_ia} vence a {hechizo_j}!")

        # --- 2. Gestionar ESCUDOS ---
        if hechizo_j == Elemento.ESCUDO:
            dano_j = 0  # Bloquea todo
            log.append("Jugador usa ESCUDO y bloquea el daño.")

        if hechizo_ia == Elemento.ESCUDO:
            dano_ia = 0
            log.append("IA usa ESCUDO y se protege.")

        # --- 3. Gestionar CURACIONES ---
        # Regla: Cura 7, pero si te pegan (dano > 0) solo cura 5.

        if hechizo_j == Elemento.CURACION:
            # Si iba a recibir daño, se reduce la cura
            cura_real = 5 if dano_j > 0 else 7
            cura_j = cura_real
            # Nota: El daño NO se anula al curar, se recibe el daño y se suma la cura
            # Si prefieres que cure neto, matemáticamente es lo mismo.
            log.append(f"Jugador se cura {cura_real} puntos.")

        if hechizo_ia == Elemento.CURACION:
            cura_real = 5 if dano_ia > 0 else 7
            cura_ia = cura_real
            log.append(f"IA se cura {cura_real} puntos.")

        # --- 4. APLICAR CAMBIOS ---
        self.jugador.recibir_daño(dano_j)
        self.ia.recibir_daño(dano_ia)
        self.jugador.curar(cura_j)
        self.ia.curar(cura_ia)

        return log

    def _gana(self, atacante, defensor):
        if atacante == Elemento.FUEGO and defensor == Elemento.PLANTA: return True
        if atacante == Elemento.PLANTA and defensor == Elemento.AGUA: return True
        if atacante == Elemento.AGUA and defensor == Elemento.FUEGO: return True
        # Si atacas a alguien curandose, le pegas (técnicamente "ganas" el intercambio de daño)
        if atacante in [Elemento.FUEGO, Elemento.AGUA, Elemento.PLANTA] and defensor == Elemento.CURACION: return True
        return False