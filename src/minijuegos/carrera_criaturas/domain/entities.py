# src/dominio/entities.py
from dataclasses import dataclass, field
from typing import List

@dataclass
class Casilla:
    posicion: int
    tipo: str = "normal"  # normal, trampa, boost
    ocupada_por: str = None  # nombre del jugador que está aquí

@dataclass
class Criatura:
    nombre: str
    posicion: int = 0
    vida: int = 100
    boosts: int = 0

@dataclass
class Jugador:
    nombre: str
    criatura: Criatura
    puntuacion: int = 0

@dataclass
class Tablero:
    casillas: List[Casilla] = field(default_factory=list)

    def __post_init__(self):
        if not self.casillas:
            self.casillas = [Casilla(pos) for pos in range(20)]  # ejemplo: 20 casillas
