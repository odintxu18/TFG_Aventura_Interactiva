import sqlite3
import random

def get_dificultad():
    """Devuelve la dificultad del rival según sus victorias previas."""
    con = sqlite3.connect("data/partidas.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS progreso (id INTEGER PRIMARY KEY, derrotas INT)")
    cur.execute("SELECT derrotas FROM progreso WHERE id=1")
    fila = cur.fetchone()
    derrotas = fila[0] if fila else 0
    con.close()
    return min(derrotas, 5)  # dificultad de 0 a 5

def registrar_derrota():
    """Incrementa la experiencia del rival (cuando te gana)."""
    con = sqlite3.connect("data/partidas.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS progreso (id INTEGER PRIMARY KEY, derrotas INT)")
    cur.execute("INSERT OR REPLACE INTO progreso (id, derrotas) VALUES (1, COALESCE((SELECT derrotas FROM progreso WHERE id=1),0)+1)")
    con.commit()
    con.close()

def decision_ia(prob_mejor_jugada=0.5):
    """La IA toma decisiones con una probabilidad de hacer el movimiento correcto."""
    return random.random() < prob_mejor_jugada

class AirHockeyAI:
    """IA adaptativa basada en tu sistema de derrotas."""

    def __init__(self):
        dificultad = get_dificultad()
        self.inteligencia = 0.3 + 0.12 * dificultad  # igual que tu tres en raya

    def mover(self, paddle, puck):
        """
        Devuelve el movimiento recomendado:
        -1 → mover a la izquierda
         1 → mover a la derecha
         0 → no moverse
        """

        # Decide si la IA hace lo óptimo o no
        if not decision_ia(self.inteligencia):
            return random.choice([-1, 0, 1])

        # Movimiento inteligente: seguir la posición del puck
        if puck.x < paddle.x:
            return -1
        elif puck.x > paddle.x:
            return 1
        return 0

