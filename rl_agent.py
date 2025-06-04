from agent import Agent
import random


class RLAgent(Agent):
    @staticmethod
    def _choose_best_move(state, q_table):
        state_str = str(state)

        for move in q_table[state_str]:
            best_move = move
            max = 0

            for arg in q_table[state_str][move]:
                best_arg = {arg[0]: arg[1]}
                if q_table[state_str][move][arg] > max:
                    max = q_table[state_str][move][arg]
                    best_move = move
                    best_arg = {arg[0]: arg[1]}

        print(f"Best move is method: {best_move} arg: {best_arg}")
        return best_move, best_arg

    def choose_move(self, possible_moves, state, ctx, q_table, epsilon):
        if (random.random() < epsilon):
            print(f"RLAGT: Choosing a random move")
            chosen_move =  random.choice(list(possible_moves.keys()))
            args = random.choice(possible_moves[chosen_move])
        else:
            print(f"RLAGT: Choosing the best move based on Q Table")
            chosen_move, args = self._choose_best_move(state["cells"], q_table)

        return chosen_move, args
    