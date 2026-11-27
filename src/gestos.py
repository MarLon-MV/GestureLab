import math

MUNECA = 0

# Diccionario: nombre del dedo -> tupla (punta, articulación media)
DEDOS = {
    "indice": (8, 6),
    "corazon": (12, 10),
    "anular": (16, 14),
    "menique": (20, 18),
}


class Gesto:
    def __init__(self, nombre):
        self.nombre = nombre

    def detectar(self, landmarks):
        # Cada clase derivada debe sobrescribir este método
        raise NotImplementedError("Cada gesto debe implementar detectar()")

    def distancia(self, punto_a, punto_b):
        return math.dist((punto_a.x, punto_a.y), (punto_b.x, punto_b.y))

    def dedo_extendido(self, landmarks, punta, articulacion):
        # Extendido: la punta está más lejos de la muñeca que la articulación
        distancia_muneca_punta = self.distancia(
            landmarks[MUNECA], landmarks[punta])
        distancia_muneca_articulacion = self.distancia(
            landmarks[MUNECA], landmarks[articulacion])
        return distancia_muneca_punta > distancia_muneca_articulacion

    def pulgar_extendido(self, landmarks):
        # El pulgar se mide desde la base del meñique (17), no desde la muñeca.
        # Su punta es el punto 4 y su articulación el punto 3.
        distancia_base_punta = self.distancia(landmarks[17], landmarks[4])
        distancia_base_articulacion = self.distancia(
            landmarks[17], landmarks[3])
        return distancia_base_punta > distancia_base_articulacion

    def contar_dedos(self, landmarks):
        total = 0

        if self.pulgar_extendido(landmarks):
            total += 1

        for punta, articulacion in DEDOS.values():
            if self.dedo_extendido(landmarks, punta, articulacion):
                total += 1

        return total


class GestoManoAbierta(Gesto):
    def __init__(self):
        super().__init__("mano_abierta")

    def detectar(self, landmarks):
        return self.contar_dedos(landmarks) == 5


class GestoPuño(Gesto):
    def __init__(self):
        super().__init__("puño")

    def detectar(self, landmarks):
        # Un puño se define como una mano cerrada, es decir, ningún dedo extendido.
        return self.contar_dedos(landmarks) == 0
