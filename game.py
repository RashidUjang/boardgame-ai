class GameState:
    def __init__(self):
        self.state = {}

    def getState(self):
        return self.state
    
    def setState(self, state):
        self.state = state

class GameContext:
    def __init__(self, turn = 0, current_player = 0, num_players = 2, gameover = False):
        self.turn = turn
        self.current_player = current_player
        self.num_players = num_players
        self.gameover = gameover

    def next_turn(self):
        self.turn += 1
        self.current_player = (self.current_player + 1) % self.num_players

    def __repr__(self):
        return (
            f"<GameContext turn={self.turn} "
            f"current_player={self.current_player} "
            f"num_players={self.num_players}>"
        )

class Game:
    def __init__(self, engine):
        self.engine = engine
        self.state = GameState()
        self.context = GameContext()

    def start(self):
        self.state = self.engine.setup()
        self.context = GameContext()
        self.moves = self.engine.moves
        self.turn_config = self.engine.turn
        self.end_condition = self.engine.end_if
        self.turns_taken = 0

        print(f"ENG: Initialized game state: {self.state}")
        print(f"ENG: Initialized moves: {self.moves}")
    
    def execute_move(self, player_id, move_name, move_args):
        self.moves[move_name](self.state, player_id, **move_args)
        print(f"ENG: Game state updated to: {self.state}")

        end = self.engine.end_if(self.state, self.context)

        if (end):
            self.context.gameover = end
            print(f"ENG: Game has ended. Results {self.context.gameover}")
            return

        if (self.turns_taken >= self.turn_config["min_moves"] & self.turns_taken <= self.turn_config["max_moves"]):
            print(f"ENG: Turn for Player {self.context.current_player} has ended")
            self.context.next_turn()
            print(f"ENG: Player {self.context.current_player} is next")
    
    def _reset_Game(self):
        self.state = GameState()
        self.context = GameContext()

    def get_state(self):
        return self.state
    
    def get_context(self):
        return self.context
    
    def get_all_moves(self):
        return self.moves

    def get_gameover_state(self):
        return self.context.gameover
    
    def get_possible_moves(self):
        possible_moves = self.engine.moves_mask(self.moves, self.state, self.context)
        return possible_moves