from google import genai

client = genai.Client(api_key="AIzaSyDH9J3uvm4ZfgopLdc9EYyOVKsc2mO8DUo")

response = client.models.generate_content(
    model="gemma-3-27b-it",
    contents="Necesito que me escribas una historia narrativa a traves de estas 3 palabras  "
             " (noche, mariposas y caracoles) en el cual tienes un rival llamado (Lucas)"
            "que tenga preguntas entremedias para conocer al jugador de la historia y que entremedias incluyas un minijuego que sea un tres en raya y un pidera papel o tijera"

)

print(response.text)
