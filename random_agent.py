import random
from agent import Agent

class RandomAgent(Agent):
    def __init__(self):
        print("Init")

    def choose_move(self, possible_moves, state, ctx):
        chosen_move =  random.choice(list(possible_moves.keys()))
        args = random.choice(possible_moves[chosen_move])
        
        return chosen_move, args
    