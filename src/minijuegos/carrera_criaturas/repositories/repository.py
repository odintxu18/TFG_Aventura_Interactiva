# src/repositorios/tablero_repo.py
from src.minijuegos.carrera_criaturas.domain.entities import Tablero


class TableroRepository:
    """Repo simple en memoria."""
    def __init__(self):
        self.tableros = {}

    def guardar(self, id_tablero: str, tablero: Tablero):
        self.tableros[id_tablero] = tablero

    def obtener(self, id_tablero: str) -> Tablero:
        return self.tableros.get(id_tablero)
