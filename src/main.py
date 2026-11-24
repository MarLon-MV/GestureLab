import cv2
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python import vision

RUTA_MODELO = "modelos/hand_landmarker.task"


def crear_detector():
    # TODO 1: crea las opciones con vision.HandLandmarkerOptions(...)
    #   - base_options=BaseOptions(model_asset_path=RUTA_MODELO)
    #   - num_hands=1
    vision_options = vision.HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=RUTA_MODELO),
        num_hands=1
    )
    # TODO 2: devuelve vision.HandLandmarker.create_from_options(opciones)
    vision_detector = vision.HandLandmarker.create_from_options(vision_options)
    return vision_detector


def dibujar_mano(fotograma, landmarks):
    # shape devuelve (alto, ancho, canales); nos quedamos con los dos primeros
    alto, ancho = fotograma.shape[:2]

    # TODO 3: recorre "landmarks" con un for (cada elemento es un punto)
    for punto in landmarks:
        #   TODO 4: convierte a píxeles: x = int(punto.x * ancho), y = int(punto.y * alto)
        x = int(punto.x * ancho)
        y = int(punto.y * alto)
    #   TODO 5: dibuja un círculo verde relleno:
        cv2.circle(fotograma, (x, y), 5, (0, 255, 0), -1)


def main():

    camara = cv2.VideoCapture(0)
    # TODO 6: antes del while, crea el detector con crear_detector()
    detector = crear_detector()

    if not camara.isOpened():
        print("No se pudo abrir la cámara.")
        return

    while True:

        ok, fotograma = camara.read()

        if not ok:
            print("No se pudo leer el fotograma.")
            break

        fotograma = cv2.flip(fotograma, 1)

       # Dentro del while, DESPUÉS del flip y ANTES del imshow:
#   TODO 7: convierte a RGB: rgb = cv2.cvtColor(fotograma, cv2.COLOR_BGR2RGB)
        rgb = cv2.cvtColor(fotograma, cv2.COLOR_BGR2RGB)
#   TODO 8: crea la imagen de MediaPipe:
#           imagen_mp = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        imagen_mp = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
#   TODO 9: resultado = detector.detect(imagen_mp)
        resultado = detector.detect(imagen_mp)
#   TODO 10: si resultado.hand_landmarks no está vacía (un simple "if lista:"),
#            llama a dibujar_mano(fotograma, resultado.hand_landmarks[0])
        if resultado.hand_landmarks:
            dibujar_mano(fotograma, resultado.hand_landmarks[0])

        cv2.imshow("GestureLab", fotograma)

        if cv2.waitKey(1) == ord("q"):
            break

    camara.release()
    # TODO 11: al final, junto a camara.release(), llama a detector.close()
    detector.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
