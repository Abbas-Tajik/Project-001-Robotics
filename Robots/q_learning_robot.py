"""
Implement a Q-Learning robot that is compatible with the get_trained_q_learning_robot function
in train_q_learner.py
"""

from random import random, randint, choice
from Robots.base_robot import BaseRobot


class QLearningRobot(BaseRobot):
    """Simulated robot that demonstrates Q-Learning."""

    def __init__(self, name='',
                 epsilon=0.99,          # probability of choosing a random action
                 decay_factor=0.99,     # rate at which epsilon decays
                 learning_rate=0.1,     # factor by which last reward affects current Q-value
                 discount_factor=0.9,   # factor by which we discount future rewards (γ: gamma)
                 min_epsilon=0.1):      # minimum value of epsilon
        super().__init__(name)
        self.epsilon = epsilon
        self.decay_factor = decay_factor
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.min_epsilon = min_epsilon
        self.last_action_number = None
        self.q_table = None
        self.initialize_q_table()

    def initialize_q_table(self):
        """Each state/action pair is assigned a small random value."""
        # Robot can see 5 squares, 3 possible values each (empty, can, wall)
        # This gives 3 ** 5 (243) possible states
        max_states = 3 ** 5
        self.q_table = [[random(), random(), random(), random(), random(), random(), random()]
                        for _ in range(max_states)]
        # Alternatively, we can initialize the Q-Table with all zeros
        # self.q_table = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] for _ in range(max_states)]

    def choose_action(self, is_learning=False):
        """
        Choose an action based on the current state of the environment and the Q-table.
        If is_learning is True, the robot will choose a random action with probability epsilon.
        Otherwise, it will choose the best known action based on the Q-table.
        """
        # situation number is an integer representing the current state
        _, situation_number = self.sense_environment()

        # If the robot is still exploring the range of possible actions rather than just
        # exploiting what it has already learned, and if a random action should be chosen
        if is_learning and self.should_choose_random_action():
            # pick a random action
            action_number = randint(0, len(self.actions) - 1)
        else:
            # Pick the best known action (or one of them if more than one)
            q_values = self.q_table[situation_number]
            max_q = max(q_values)
            best_actions = [action for action in range(len(q_values))
                            if q_values[action] == max_q]
            action_number = choice(best_actions)

        self.last_action_number = action_number
        # Return the chosen action
        return self.actions[action_number]

    def should_choose_random_action(self):
        """Decide to choose a random action if a random value [0..1) <= epsilon."""
        return random() <= self.epsilon

    def decay_epsilon(self):
        """
        Make the robot less likely to pick random actions during learning while ensuring that
        there is still some small chance of choosing random actions.
        """
        self.epsilon = max(self.epsilon * self.decay_factor, self.min_epsilon)

    def reinforce(self, reward):
        """Apply the Q-Learning formula."""
        assert self.last_action_number is not None

        situation_number_before_action = self.situation_number
        current_q_value = self.q_table[situation_number_before_action][self.last_action_number]

        # Calculate the new Q-value
        # Q(s, a) <- Q(s, a) + α * (r + γ * max(Q(s', a')) - Q(s, a))
        max_next_q = self.calculate_max_q_next_state()
        new_q_value = current_q_value + \
            self.learning_rate * (reward + self.discount_factor * max_next_q - current_q_value)

        # Update the Q-table with new Q-value
        self.q_table[situation_number_before_action][self.last_action_number] = new_q_value

    def calculate_max_q_next_state(self):
        """
        # Q(s, a) <- Q(s, a) + α * (r + γ * max(Q(s', a')) - Q(s, a))
        # In this function we calculate the max(Q(s', a')) part.
        """

        # Get the new environment configuration following the most recent action
        _, situation_number_after_action = self.sense_environment()

        possible_next_q_values = self.q_table[situation_number_after_action]
        max_next_q = max(possible_next_q_values)
        return max_next_q
