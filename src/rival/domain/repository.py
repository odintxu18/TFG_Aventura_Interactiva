from abc import ABC, abstractmethod


class RivalRepository(ABC):
  

    @abstractmethod
    def obtener_derrotas(self) -> int:
        pass

    @abstractmethod
    def registrar_derrota(self):
        pass