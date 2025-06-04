from game import Game
from tictactoe import TicTacToeEngine
from rl_agent import RLAgent
from random_agent import RandomAgent
from ql import QLearning
import random
import time
import copy

ticTacToeEngine = TicTacToeEngine()
game = Game(ticTacToeEngine)
rl_agent = RLAgent()
random_agent = RandomAgent()
ql = QLearning()

agent_wins = 0
random_agent_wins = 0
draws = 0

num_episodes = int(1e7)

start = time.perf_counter()
print('Start training...')

for episode in range(num_episodes):
    game.start()

    agent_player_id = 0 if random.random() < 0.5 else 1
    random_agent_player_id = 0 if agent_player_id == 1 else 1

    rl_agent.set_player_id(agent_player_id)
    random_agent.set_player_id(random_agent_player_id)

    turn_map = {
        agent_player_id: rl_agent,
        random_agent_player_id: random_agent
    }

    new_state = None
    old_state = None
    chosen_move = None
    args = None

    while game.get_gameover_state() is False:
        ql.init_state_in_q_table(game.get_state()["cells"], game.get_possible_moves()) 

        current_player_id = game.get_context().current_player
        print(f"The current player is {current_player_id}")

        current_player = turn_map[current_player_id]
        print(current_player)

        if (isinstance(current_player, RLAgent)):
            chosen_move, args = current_player.choose_move(
                game.get_possible_moves(), game.get_state(), game.get_context(), ql.get_q_table(), ql.get_ql_config()["epsilon"])
        else:
            chosen_move, args = current_player.choose_move(
                game.get_possible_moves(), game.get_state(), game.get_context())
        
        # Copy needed as it is referencing the same value
        old_state = copy.deepcopy(game.get_state())

        print(f"Player chose move {(chosen_move, args)}")
        game.execute_move(current_player_id, chosen_move, args)

        new_state = game.get_state()

        ql.init_state_in_q_table(new_state["cells"], game.get_possible_moves())
        ql.update_q_table(old_state["cells"], new_state["cells"], chosen_move, args, 0)

    game_result = game.get_gameover_state()

    if (game_result["winner"] == "draw"):
        reward = 0.1
        draws += 1
    elif (game_result["winner"] == agent_player_id):
        reward = 1
        agent_wins += 1
    else:
        reward = -1
        random_agent_wins += 1
    
    print(f"Reward is {reward}")

    ql.update_q_table(old_state["cells"], new_state["cells"], chosen_move, args, reward)
    ql.decay_epsilon()


end = time.perf_counter()

print(f"-------Training has ended Elapsed time: {end - start} seconds-------")
print(f"Agent wins: {agent_wins}")
print(f"Random Agent wins: {random_agent_wins}")
print(f"Draws: {draws}")
