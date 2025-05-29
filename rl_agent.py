from agent import Agent
import random

class RLAgent(Agent):
    def __init__(self, learning_rate = 0.2, discount_factor = 0.9, epsilon = 1.0, epsilon_min = 0.01, epsilon_decay = 0.999):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay


    def choose_move(self, possible_moves, state, ctx):
        chosen_move =  random.choice(list(possible_moves.keys()))
        args = random.choice(possible_moves[chosen_move])

        return chosen_move, args