from json import load
from mss import mss
import cv2
import numpy as np

# Alcance de la matriz para detectar las piezas
MATRIX_SCOPE = 3


class Environment:
    def __init__(self):
        self.sct = mss()
        self.rows = 22
        self.columns = 10

        try:
            with open("dimensions.json", "r") as f:
                self.monitor = load(f)
        except FileNotFoundError:
            print(
                "ERROR: No se encontró 'dimensions.json'. Ejecuta 'generate_dimensions.py' primero."
            )
            exit()

    def capture_screen_board(self):
        sct_img = self.sct.grab(self.monitor)
        img = np.array(sct_img)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        return img_bgr

    def get_matrix_board(self, img, save_debug=False):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        debug_img = img.copy() if save_debug else None
        img_height, img_width = img_gray.shape
        cell_height = img_height / self.rows
        cell_width = img_width / self.columns

        matrix = np.zeros((self.rows, self.columns), dtype=int)
        margin_y = int(cell_height * 0.25)
        margin_x = int(cell_width * 0.25)

        for row in range(self.rows):
            for col in range(self.columns):
                y_start = int(row * cell_height) + margin_y
                y_end = int((row + 1) * cell_height) - margin_y
                x_start = int(col * cell_width) + margin_x
                x_end = int((col + 1) * cell_width) - margin_x

                roi = img_gray[y_start:y_end, x_start:x_end]
                promedio_brillo = np.mean(roi)
                if promedio_brillo > 50:
                    matrix[row][col] = 1
                    color_caja = (0, 255, 0)
                else:
                    matrix[row][col] = 0
                    color_caja = (0, 0, 255)

                if save_debug:
                    cv2.rectangle(
                        debug_img, (x_start, y_start), (x_end, y_end), color_caja, 1
                    )

        if save_debug:
            cv2.imwrite("debug_tablero.png", debug_img)

        return matrix[2:], matrix[:MATRIX_SCOPE]

    def get_piece(self, matrix):
        filas_ocupadas, cols_ocupadas = np.where(matrix == 1)

        if len(filas_ocupadas) == 0:
            return None, None

        min_f, max_f = np.min(filas_ocupadas), np.max(filas_ocupadas)
        min_c, max_c = np.min(cols_ocupadas), np.max(cols_ocupadas)

        forma_detectada = matrix[min_f : max_f + 1, min_c : max_c + 1].tolist()

        formas_piezas = {
            "I": [[1, 1, 1, 1]],
            "O": [[1, 1], [1, 1]],
            "T": [
                [0, 1, 0],
                [1, 1, 1],
            ],
            "J": [
                [1, 0, 0],
                [1, 1, 1],
            ],
            "L": [
                [0, 0, 1],
                [1, 1, 1],
            ],
            "S": [
                [0, 1, 1],
                [1, 1, 0],
            ],
            "Z": [
                [1, 1, 0],
                [0, 1, 1],
            ],
        }

        for nombre, forma in formas_piezas.items():
            if forma_detectada == forma:
                return forma, nombre

        return None, None

    def close(self):
        self.sct.close()
