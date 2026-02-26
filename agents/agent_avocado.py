import copy
from time import sleep
from pynput.keyboard import Controller, Key


class AgentAvocado:
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

    def rotate_shape(self, shape):
        return [list(row) for row in zip(*shape[::-1])]

    def check_collision(self, board, shape, offset_x, offset_y):
        for cy, row in enumerate(shape):
            for cx, cell in enumerate(row):
                if cell:
                    x = offset_x + cx
                    y = offset_y + cy
                    if x < 0 or x >= 10 or y >= 20 or y < 0 or board[y][x]:
                        return True
        return False

    def get_drop_y(self, board, shape, offset_x):
        y = 0
        while not self.check_collision(board, shape, offset_x, y):
            y += 1
        return y - 1

    def evaluate_board(self, board):
        heights = [0] * 10
        holes = 0

        for x in range(10):
            found_block = False
            for y in range(20):
                if board[y][x]:
                    if not found_block:
                        heights[x] = 20 - y
                        found_block = True
                elif found_block:
                    holes += 1

        aggregate_height = sum(heights)
        bumpiness = sum(abs(heights[i] - heights[i + 1]) for i in range(9))

        lines_cleared = 0
        for y in range(20):
            if all(board[y][x] for x in range(10)):
                lines_cleared += 1

        score = (
            (76.18 * lines_cleared)
            - (35.66 * aggregate_height)
            - (35.66 * holes)
            - (18.44 * bumpiness)
        )
        return score

    def play(self, matrix, piece_sharp, piece_name):
        if not piece_sharp:
            return

        best_score = float("-inf")
        best_x = 0
        best_rotations = 0

        SPAWN_X = 3

        max_rotations = (
            1 if piece_name == "O" else (2 if piece_name in ["I", "Z", "S"] else 4)
        )

        for rotations in range(max_rotations):
            shape_to_test = piece_sharp
            for _ in range(rotations):
                shape_to_test = self.rotate_shape(shape_to_test)

            piece_width = len(shape_to_test[0])

            for x in range(10 - piece_width + 1):
                drop_y = self.get_drop_y(matrix, shape_to_test, x)

                if drop_y < 0:
                    continue

                simulated_board = copy.deepcopy(matrix)
                for cy, row in enumerate(shape_to_test):
                    for cx, cell in enumerate(row):
                        if cell:
                            simulated_board[drop_y + cy][x + cx] = 1

                score = self.evaluate_board(simulated_board)
                if score > best_score:
                    best_score = score
                    best_x = x
                    best_rotations = rotations

        spawn = SPAWN_X
        if piece_name == "O":
            spawn = SPAWN_X + 1
        elif piece_name == "I" and best_rotations == 1:
            spawn = SPAWN_X + 2
        elif piece_name in ["L", "J", "T", "S", "Z"] and best_rotations == 1:
            spawn = SPAWN_X + 1

        offset = best_x - spawn
        direction = "right" if offset > 0 else "left"
        times = abs(offset)

        self.move(direction, times, best_rotations)
