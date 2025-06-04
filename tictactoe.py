class TicTacToeEngine:
    # Setup method must return a dictionary
    @staticmethod
    def setup():
        return {"cells": [None] * 9}

    @staticmethod
    def _click_cell(game_state, player_id, cell_id):
        game_state["cells"][cell_id] = player_id

    turn = {
        "min_moves": 1,
        "max_moves": 1
    }

    moves = {
        "click_cell": _click_cell,
    }

    @staticmethod
    def _is_row_complete(state, position):
        # For every number in a winning position, get the board's value
        symbols = [state["cells"][i] for i in position]

        # Check that all of the symbol is not null and not equal to the first of the value
        return all(symbol is not None and symbol == symbols[0] for symbol in symbols)

    def _is_victory(self, state):
        winning_positions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
            [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]
        ]

        return any(self._is_row_complete(state, position) for position in winning_positions)
    
    def _is_draw(self, state):
        return all(position is not None for position in state["cells"])

    def end_if(self, game_state, game_context):
        vic = self._is_victory(game_state)
        draw = self._is_draw(game_state)

        if (vic):
            return {"winner": game_context.current_player}
        
        if (draw):
            return {"winner": "draw"}
        return False
    
    def moves_mask(self, all_moves, game_state, game_context):
        masked_moves = {}
        available_cells = []

        for move in all_moves:
            for index, cell in enumerate(game_state["cells"]):
                if cell is None:
                    available_cells.append({"cell_id": index})

            masked_moves[move] = available_cells
        return masked_moves