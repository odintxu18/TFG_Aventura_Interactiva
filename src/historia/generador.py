import os
import requests

API_KEY = os.getenv("NAPKIN_API_KEY")  # define esta variable en tu sistema
API_URL = "https://api.napkin.ai/v1/generate"

def generar_historia(palabra, jugador, rival):
    prompt = f"""
    Crea una historia breve y épica basada en la palabra '{palabra}'.
    El protagonista es {jugador} y su rival es {rival}.
    Termina con un conflicto que pueda resolverse en un minijuego.
    """

    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {"prompt": prompt, "max_tokens": 300}

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json().get("text", "No se pudo generar historia.")
    except Exception as e:
        return f"[Error generando historia: {e}]"
