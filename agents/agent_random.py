from time import sleep
from random import randint
from pynput.keyboard import Key, Controller


class AgentRandom:
    def __init__(self):
        self.keyboard = Controller()

    def play(self, matrix, piece_sharp, piece_name):
        r1 = randint(0, 4)  # number of blocks to move
        r2 = randint(0, 1)  # 0 = left, 1 = right
        r3 = randint(0, 3)  # number of rotations

        for i in range(r3):
            self.keyboard.press(Key.up)
            sleep(0.01)
            self.keyboard.release(Key.up)

        for i in range(r1):
            if r2 == 0:
                self.keyboard.press(Key.left)
                self.keyboard.release(Key.left)
            else:
                self.keyboard.press(Key.right)
                self.keyboard.release(Key.right)

        self.keyboard.press(Key.space)
        sleep(0.01)
        self.keyboard.release(Key.space)
