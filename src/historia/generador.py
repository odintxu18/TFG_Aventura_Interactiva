import os
import google.generativeai as genai







genai.configure(api_key="AIzaSyDH9J3uvm4ZfgopLdc9EYyOVKsc2mO8DUo")



def generar_historia(palabra1, palabra2, palabra3, jugador, rival):
    prompt = f"""
    Crea una historia breve y épica basada en las palabras '{palabra1}', '{palabra2}', '{palabra3}'.
    El protagonista es {jugador} y su rival es {rival}.
    Termina con un conflicto que pueda resolverse en un minijuego.
    """

    try:
        modelo = genai.GenerativeModel("gemma-3-4b-it")
        response = modelo.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[Error generando historia: {e}]"