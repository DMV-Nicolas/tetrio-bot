from time import sleep
from environment import Environment
from agents.agent_random import AgentRandom
from agents.agent_test import AgentTest
from agents.agent_avocado import AgentAvocado

if __name__ == "__main__":
    env = Environment()
    agent = AgentTest()

    print("¡El agente empezará en 3 segundos! Cambia a la ventana de Tetrio...")
    sleep(3)

    try:
        while True:
            img = env.capture_screen_board()
            main_matrix, top_matrix = env.get_matrix_board(img)
            piece_sharp, piece_name = env.get_piece(top_matrix)
            agent.play(main_matrix, piece_sharp, piece_name)
    except KeyboardInterrupt:
        print("\nDeteniendo agente...")
        env.close()
