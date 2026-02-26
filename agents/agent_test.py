from time import sleep
from pynput.keyboard import Key, Controller


class AgentTest:
    def __init__(self):
        self.keyboard = Controller()

    def move(self, direction, times, rotations=0):
        for _ in range(rotations):
            self.keyboard.press(Key.up)
            self.keyboard.release(Key.up)

        tecla = Key.left if direction == "left" else Key.right
        for _ in range(times):
            self.keyboard.press(tecla)
            self.keyboard.release(tecla)
        sleep(0.05)

        self.keyboard.press(Key.space)
        self.keyboard.release(Key.space)
        sleep(0.08)

    def play(self, matrix, piece_sharp, piece_name):
        if piece_name == "I":
            self.move("left", 3)
        elif piece_name == "O":
            self.move("left", 4)
        elif piece_name == "T":
            self.move("left", 3, 0)
        elif piece_name == "J":
            self.move("right", 3, 3)
        elif piece_name == "L":
            self.move("right", 0, 1)
        elif piece_name == "S":
            self.move("right", 4, 1)
        elif piece_name == "Z":
            self.move("right", 4, 1)
        sleep(0.2)
