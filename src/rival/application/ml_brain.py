import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from src.rival.infraestructure.sqlite_repository import SQLiteRivalRepository


class RivalBrain:
    def __init__(self, repository: SQLiteRivalRepository):
        self.repository = repository
        self.model = RandomForestClassifier(n_estimators=10, max_depth=3)
        self.is_trained = False
        self.estilo_jugador_predicho = "Normal"  # Default

    def entrenar(self):
        """
        Toma los datos de la BBDD y entrena un modelo para predecir
        si el jugador gana o pierde basándose en su agresividad.
        """
        df = self.repository.obtener_dataframe_stats()

        # Necesitamos al menos 3 partidas para empezar a 'aprender' algo útil
        if len(df) < 3:
            return

        # FEATURES (X): Cómo jugó el humano
        X = df[['agresividad', 'velocidad', 'errores']]

        # TARGET (y): ¿Ganó el humano? (Queremos predecir qué hace que gane)
        # Convertimos 'X'/'O' a 1/0
        y = df['resultado'].apply(lambda r: 1 if r == 'X' else 0)

        try:
            self.model.fit(X, y)
            self.is_trained = True

            # Analizamos el perfil promedio del jugador
            avg_aggro = df['agresividad'].mean()
            if avg_aggro > 0.7:
                self.estilo_jugador_predicho = "Agresivo"
            elif avg_aggro < 0.3:
                self.estilo_jugador_predicho = "Defensivo"
            else:
                self.estilo_jugador_predicho = "Equilibrado"

        except Exception as e:
            print(f"[ML Warning] No hay datos suficientes para entrenar: {e}")

    def obtener_contramedida(self) -> dict:
        """
        Devuelve parámetros de configuración para la IA (Adaptadores)
        basados en el aprendizaje.
        """
        self.entrenar()  # Re-entrena con los últimos datos

        config = {
            "agresividad_ia": 0.5,
            "tasa_error_ia": 0.2
        }

        if not self.is_trained:
            return config  # Configuración por defecto

        # ESTRATEGIA DE CONTRA-ATAQUE (Counter-Play)
        if self.estilo_jugador_predicho == "Agresivo":
            # Si el jugador es agresivo, la IA juega defensiva y segura (espera el error)
            config["agresividad_ia"] = 0.2
            config["tasa_error_ia"] = 0.05  # Juega muy preciso
            print("IA: Detecto agresividad. Activando modo Muro Defensivo.")

        elif self.estilo_jugador_predicho == "Defensivo":
            # Si el jugador es defensivo, la IA debe ser hiper-agresiva para romperlo
            config["agresividad_ia"] = 0.9
            config["tasa_error_ia"] = 0.15
            print("IA: Detecto pasividad. Activando modo Berserker.")

        else:
            # Equilibrado
            config["agresividad_ia"] = 0.6
            print("IA: Jugador equilibrado. Adaptación estándar.")

        return config