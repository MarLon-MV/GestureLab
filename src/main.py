import cv2


def main():
    # TODO 1: abre la cámara 0 con cv2.VideoCapture y guárdala en "camara"
    camara = cv2.VideoCapture(0)
    # TODO 2: si la cámara no se abrió (camara.isOpened() es False),
    #         imprime un aviso y haz "return" para salir
    if not camara.isOpened():
        print("No se pudo abrir la cámara.")
        return 
    
    while True:
        # TODO 3: lee un fotograma:  ok, fotograma = camara.read()
        ok, fotograma = camara.read()

        # TODO 4: si ok es False, imprime un aviso y sal del bucle con "break"
        if not ok:
            print("No se pudo leer el fotograma.")
            break
        # TODO 5: voltea el fotograma como un espejo: cv2.flip(fotograma, 1)
        fotograma = cv2.flip(fotograma, 1)
        # TODO 6: muestra el fotograma: cv2.imshow("GestureLab", fotograma)
        cv2.imshow("GestureLab", fotograma)
        # TODO 7: si cv2.waitKey(1) == ord("q"), sal del bucle con "break"
        if cv2.waitKey(1) == ord("q"):
            break

    # TODO 8: libera la cámara y cierra las ventanas (cv2.destroyAllWindows())
    camara.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
