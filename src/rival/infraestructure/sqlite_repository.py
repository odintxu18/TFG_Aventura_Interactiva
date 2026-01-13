import sqlite3
import pandas as pd
from src.rival.domain.repository import RivalRepository

class SQLiteRivalRepository(RivalRepository):
    def __init__(self, db_path="data/partidas.db"):
        self.db_path = db_path
        self._inicializar_tabla()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _inicializar_tabla(self):
        with self._get_connection() as con:
            con.execute("CREATE TABLE IF NOT EXISTS progreso (id INTEGER PRIMARY KEY, derrotas INT)")
            # NUEVA TABLA PARA ML
            con.execute("""
                CREATE TABLE IF NOT EXISTS match_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_type TEXT,
                    agresividad FLOAT,  -- 0.0 a 1.0 (Defensivo -> Ofensivo)
                    velocidad FLOAT,    -- Acciones por segundo
                    errores INT,        -- Fallos no forzados
                    resultado TEXT      -- 'X' (Gano Jugador) o 'O' (Gano IA)
                )
            """)
    def obtener_derrotas(self) -> int:
        with self._get_connection() as con:
            cur = con.cursor()
            cur.execute("SELECT derrotas FROM progreso WHERE id=1")
            fila = cur.fetchone()
            return fila[0] if fila else 0

    def registrar_derrota(self):
        with self._get_connection() as con:
            # Usamos lógica de UPSERT (Insert or Replace)
            con.execute("""
                INSERT OR REPLACE INTO progreso (id, derrotas) 
                VALUES (1, COALESCE((SELECT derrotas FROM progreso WHERE id=1), 0) + 1)
            """)

    def guardar_stats(self, game_type, agresividad, velocidad, errores, resultado):
        """Guarda una fila de datos para que la IA aprenda."""
        with self._get_connection() as con:
            con.execute("""
                INSERT INTO match_stats (game_type, agresividad, velocidad, errores, resultado)
                VALUES (?, ?, ?, ?, ?)
            """, (game_type, agresividad, velocidad, errores, resultado))

    def obtener_dataframe_stats(self):
        """Devuelve todos los datos en formato Pandas para Scikit-Learn."""
        with self._get_connection() as con:
            return pd.read_sql_query("SELECT * FROM match_stats", con)