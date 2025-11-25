from src.minijuegos.magos.domain.spell import Hechizo


class Batalla:
    def __init__(self, mago1, mago2):
        self.mago1 = mago1
        self.mago2 = mago2
        self.turno = 1

    def resolver_turno(self, hechizo1: Hechizo, hechizo2: Hechizo):
        # Primero, aplicar efectos simultáneos
        resultados = []

        for mago, enemigo, hechizo in [(self.mago1, self.mago2, hechizo1), (self.mago2, self.mago1, hechizo2)]:
            if hechizo.tipo == "ataque":
                enemigo.aplicar_daño(hechizo.valor)
                resultados.append(f"{mago.nombre} lanza {hechizo.nombre} causando {hechizo.valor} de daño.")
            elif hechizo.tipo == "escudo":
                mago.activar_escudo(hechizo.valor)
                resultados.append(f"{mago.nombre} se protege con un escudo de {hechizo.valor}.")
            elif hechizo.tipo == "curacion":
                mago.curar(hechizo.valor)
                resultados.append(f"{mago.nombre} se cura {hechizo.valor} de energía.")
            elif hechizo.tipo == "riesgo":
                enemigo.aplicar_daño(hechizo.valor)
                mago.aplicar_daño(int(hechizo.valor * 0.3))
                resultados.append(f"{mago.nombre} lanza un hechizo riesgoso ({hechizo.valor} de daño, recibe 30%).")

        self.turno += 1
        return resultados
