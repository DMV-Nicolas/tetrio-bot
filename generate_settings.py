import mss
import cv2
import numpy as np
import json
from time import sleep


def generate_settings():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)

        img = np.array(sct_img)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    print("\n--- INSTRUCCIONES ---")
    print(
        "1. Dibuja un rectángulo exactamente sobre el área de juego (sin bordes externos)."
    )
    print("2. Presiona 'ENTER' o 'ESPACIO' para confirmar la selección.")
    print("3. Presiona 'C' para cancelar y salir.")
    print("---------------------\n")

    cv2.namedWindow("Selecciona el tablero de Tetrio", cv2.WINDOW_NORMAL)
    roi = cv2.selectROI(
        "Selecciona el tablero de Tetrio", img_bgr, fromCenter=False, showCrosshair=True
    )
    cv2.destroyAllWindows()

    x, y, w, h = roi
    cell_height = h / 20

    if w > 0 and h > 0:
        settings = {
            "top": int(y - cell_height * 2),
            "left": int(x),
            "width": int(w),
            "height": int(h + cell_height * 2),
        }

        with open("settings.json", "w") as archivo_json:
            json.dump(settings, archivo_json, indent=4)
        print("¡Éxito! Configuración guardada en 'settings.json'.")
        print(f"Valores guardados: {settings}")
    else:
        print("Selección cancelada. No se guardó ningún archivo.")


def set_window():
    print("Cambia a la ventana de Tetrio! Se iniciará en 3 segundos...")
    sleep(3)


def look_settings():
    with open("settings.json", "r") as f:
        config = json.load(f)
    sct = mss.mss()
    monitor = config

    while True:
        sct_img = sct.grab(monitor)
        img = np.array(sct_img)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        cv2.imshow("Vista del agente", img_bgr)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    set_window()
    generate_settings()
    look_settings()
