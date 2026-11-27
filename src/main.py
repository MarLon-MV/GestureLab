import cv2
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python import vision

from gestos import GestoManoAbierta, GestoPuño

RUTA_MODELO = "modelos/hand_landmarker.task"


def crear_detector():

    vision_options = vision.HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=RUTA_MODELO),
        num_hands=1
    )

    vision_detector = vision.HandLandmarker.create_from_options(vision_options)
    return vision_detector


def dibujar_mano(fotograma, landmarks):
    # shape devuelve (alto, ancho, canales); nos quedamos con los dos primeros
    alto, ancho = fotograma.shape[:2]

    for punto in landmarks:
        x = int(punto.x * ancho)
        y = int(punto.y * alto)

        cv2.circle(fotograma, (x, y), 5, (0, 255, 0), -1)


def main():

    camara = cv2.VideoCapture(0)

    if not camara.isOpened():
        print("No se pudo abrir la cámara.")
        return

    detector = crear_detector()
    gesto = GestoPuño()

    while True:

        ok, fotograma = camara.read()

        if not ok:
            print("No se pudo leer el fotograma.")
            break

        fotograma = cv2.flip(fotograma, 1)

        rgb = cv2.cvtColor(fotograma, cv2.COLOR_BGR2RGB)

        imagen_mp = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        resultado = detector.detect(imagen_mp)

        if resultado.hand_landmarks:
            dibujar_mano(fotograma, resultado.hand_landmarks[0])
            if gesto.detectar(resultado.hand_landmarks[0]):
                cv2.putText(fotograma, gesto.nombre, (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("GestureLab", fotograma)

        if cv2.waitKey(1) == ord("q"):
            break

    camara.release()
    detector.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
