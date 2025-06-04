class QLearning:
    def __init__(self, learning_rate=0.2, discount_factor=0.9, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.999):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.q_table = {}

    def init_state_in_q_table(self, state, possible_moves):
        print(f"QL: Checking if state needs to be added in Q Table")
        state_str = str(state)

        if state_str not in self.q_table:
            print(f"QL: Adding {state_str} to the Q Table")
            # Initialize the outer dict for this state
            self.q_table[state_str] = {}

            for key in possible_moves.keys():
                if key not in self.q_table[state_str]:
                    # Initialize the dict for the key
                    self.q_table[state_str][key] = {}

                for move in possible_moves[key]:
                    move_tuple = list(move.items())[0]
                    self.q_table[state_str][key][move_tuple] = 0
        else:
            print(f"QL: No update needed")

    def update_q_table(self, old_state, new_state, action, args, reward):
        print(f"QL: Applying Bellman's Equation")
        old_state_str = str(old_state)
        new_state_str = str(new_state)

        # Convert args to tuple
        move_in_tuple = list(args.items())[0]

        max_q_value_for_action = self._get_max_q_table(
            self.q_table[new_state_str], action)

        self.q_table[old_state_str][action][move_in_tuple] += self.learning_rate * (
            reward + self.discount_factor * max_q_value_for_action - self.q_table[old_state_str][action][move_in_tuple])
        
        print("QL: Updated {old_state_str} value to {self.q_table[old_state_str][action][move_in_tuple]}")

    @staticmethod
    def _get_max_q_table(table, action):
        args = table[action]

        max_value = 0
        max_key = None

        for key, value in args.items():
            max_key = key
            if (value > max_value):
                max_key = key
                max_value = value

        return max_value

    def get_q_table(self):
        return self.q_table

    def get_ql_config(self):
        return {"learning_rate": self.learning_rate,
                "discount_factor": self.discount_factor,
                "epsilon": self.epsilon,
                "epsilon_min": self.epsilon_min,
                "epsilon_decay": self.epsilon_decay}

    def decay_epsilon(self):
        print(f"QL: Decaying epsilon. Current epsilon value: {self.epsilon}")
        new_epsilon = max(self.epsilon_min, self.epsilon_decay * self.epsilon)
        print(f"QL: New epsilon value: {new_epsilon}")
        self.epsilon = new_epsilon
        return
