from game import Game
from tictactoe import TicTacToeEngine
from rl_agent import RLAgent
from random_agent import RandomAgent
import random
import time

ticTacToeEngine = TicTacToeEngine()
game = Game(ticTacToeEngine)
rl_agent = RLAgent()
random_agent = RandomAgent()

# num_episodes = int(1000)
num_episodes = int(2)

start = time.perf_counter()
print('Start training...')

for episode in range(num_episodes):
    game.start()

    agent_player_number = 0 if random.random() < 0.5 else 1
    random_agent_player_number = 0 if agent_player_number == 1 else 1

    rl_agent.set_player_id(agent_player_number)
    random_agent.set_player_id(random_agent_player_number)

    turn_map = {
        agent_player_number: rl_agent,
        random_agent_player_number: random_agent
    }

    while game.get_gameover_state() is False:
        current_player_id = game.get_context().current_player
        print(f"The current player is {current_player_id}")

        current_player = turn_map[current_player_id]
        print(current_player)

        chosen_move, args = current_player.choose_move(game.get_possible_moves(), game.get_state(), game.get_context())
        print(f"Player chose move {chosen_move}, {args}")
        game.execute_move(current_player_id, chosen_move, args)

end = time.perf_counter()

print(f"Elapsed time: {end - start} seconds")