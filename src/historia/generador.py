import os
import google.generativeai as genai







genai.configure(api_key="AIzaSyDH9J3uvm4ZfgopLdc9EYyOVKsc2mO8DUom")


def generar_siguiente_capitulo(contexto_previo, resultado_anterior, palabra1, palabra2, palabra3, jugador, rival,
                               n_capitulo):
    """
    Genera SOLO el siguiente fragmento de la historia basándose en si ganaste o perdiste.
    """

    # 1. Definimos la consecuencia del minijuego anterior
    if resultado_anterior == "Victoria":
        situacion = f"{jugador} ha superado el desafío contra {rival} y avanza con ventaja."
        tono = "épico y triunfal"
    elif resultado_anterior == "Derrota":
        situacion = f"{rival} ha vencido a {jugador} en el último desafío. {jugador} está herido o en desventaja."
        tono = "tenso, oscuro y desesperado"
    else:
        situacion = f"La aventura de {jugador} comienza. El conflicto con {rival} es inminente."
        tono = "misterioso e introductorio"

    # 2. TU PROMPT ORIGINAL ADAPTADO A FORMATO EPISÓDICO
    prompt = f"""
    Actúa como el narrador de un videojuego de aventura interactiva (Capítulo {n_capitulo}).

    CONTEXTO DE LA AVENTURA:
    Protagonista: {jugador}.
    Rival/Antagonista: {rival}.
    Palabras clave obligatorias (si no están en español, tradúcelas y úsalas): '{palabra1}', '{palabra2}', '{palabra3}'.

    SITUACIÓN ACTUAL (LO QUE ACABA DE PASAR):
    {situacion}

    RESUMEN DE LA HISTORIA HASTA AHORA:
    "{contexto_previo}"

    TU TAREA:
    Escribe SOLO la continuación de la historia (máximo 150-200 palabras y que no se corten).
    Usa el tono {tono}.

    IMPORTANTE:
    - NO termines la historia (a menos que el jugador muera, pero eso lo decide el juego).
    - NO des opciones A/B/C.
    - Termina el texto justo cuando aparezca un NUEVO OBSTÁCULO o ENFRENTAMIENTO que requiera habilidad.
    - NO escribas la etiqueta [MINIJUEGO], el sistema lo hará por ti.
    """

    try:
        # Usamos tu modelo
        modelo = genai.GenerativeModel("gemma-3-4b-it")
        response = modelo.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"La niebla cubre el camino... {rival} se ríe a lo lejos. (Error IA: {e})"