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
        # TODO 1: guarda el nombre en self.nombre
        self.nombre = nombre

    def detectar(self, landmarks):
        # TODO 2: lanza el error con
        #   raise NotImplementedError("Cada gesto debe implementar detectar()")
        raise NotImplementedError("Cada gesto debe implementar detectar()")

    def distancia(self, punto_a, punto_b):
        # TODO 3: devuelve math.dist((punto_a.x, punto_a.y), (punto_b.x, punto_b.y))
        return math.dist((punto_a.x, punto_a.y), (punto_b.x, punto_b.y))

    def dedo_extendido(self, landmarks, punta, articulacion):
        # TODO 4: devuelve True si la distancia de la muñeca a la punta
        #   es MAYOR que la de la muñeca a la articulación.
        #   Los puntos son landmarks[MUNECA], landmarks[punta], landmarks[articulacion]
        distancia_muneca_punta = self.distancia(
            landmarks[MUNECA], landmarks[punta])
        distancia_muneca_articulacion = self.distancia(
            landmarks[MUNECA], landmarks[articulacion])
        return distancia_muneca_punta > distancia_muneca_articulacion

    def pulgar_extendido(self, landmarks):
        # TODO 5: igual que el anterior, pero mide desde landmarks[17]
        #   (base del meñique): punta = landmarks[4], articulación = landmarks[3]
        distancia_base_punta = self.distancia(landmarks[17], landmarks[4])
        distancia_base_articulacion = self.distancia(
            landmarks[17], landmarks[3])
        return distancia_base_punta > distancia_base_articulacion


class GestoManoAbierta(Gesto):
    def __init__(self):
        # TODO 6: llama a super().__init__("mano_abierta")
        super().__init__("mano_abierta")

    def detectar(self, landmarks):
        # TODO 7: si el pulgar NO está extendido, devuelve False
        if not self.pulgar_extendido(landmarks):
            return False
        # TODO 8: recorre el diccionario con
        #   for nombre, (punta, articulacion) in DEDOS.items():
        #   y si algún dedo NO está extendido, devuelve False
        for punta, articulacion in DEDOS.items():
            if not self.dedo_extendido(landmarks, punta, articulacion):
                return False
        # TODO 9: si llegó hasta aquí, todos están extendidos: devuelve True
        return True
