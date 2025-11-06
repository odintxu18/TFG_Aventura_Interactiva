import sqlite3

def get_dificultad():
    con = sqlite3.connect("data/partidas.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS progreso (id INTEGER PRIMARY KEY, derrotas INT)")
    cur.execute("SELECT derrotas FROM progreso WHERE id=1")
    fila = cur.fetchone()
    derrotas = fila[0] if fila else 0
    con.close()
    return derrotas

def registrar_derrota():
    con = sqlite3.connect("data/partidas.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS progreso (id INTEGER PRIMARY KEY, derrotas INT)")
    cur.execute("INSERT OR REPLACE INTO progreso (id, derrotas) VALUES (1, COALESCE((SELECT derrotas FROM progreso WHERE id=1),0)+1)")
    con.commit()
    con.close()
