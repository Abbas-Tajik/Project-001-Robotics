import numpy as np
from Robots.base_robot import BaseRobot


class LookupTableRobot(BaseRobot):
    def __init__(self, name='', action_lookup_table=None):
        super().__init__(name)
        if action_lookup_table is None:
            # This default lookup table is the result of evolving the
            # robot controller using a genetic algorithm.
            action_lookup_table = np.array(
                [1, 1, 4, 3, 3, 3, 4, 4, 4, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 5, 5,
                 5, 5, 1, 1, 5, 3, 4, 4, 4, 4, 4, 0, 2, 3, 4, 0, 0, 0, 4, 0, 5,
                 5, 0, 0, 5, 5, 1, 0, 3, 3, 1, 1, 2, 2, 5, 2, 3, 1, 1, 4, 6, 4,
                 0, 2, 0, 0, 3, 6, 3, 1, 1, 5, 3, 3, 2, 1, 2, 1, 3, 3, 2, 4, 4,
                 4, 1, 5, 4, 2, 4, 2, 2, 0, 0, 0, 2, 0, 0, 0, 3, 5, 1, 6, 2, 0,
                 5, 3, 4, 1, 1, 4, 4, 0, 4, 2, 0, 4, 4, 0, 0, 2, 4, 5, 2, 2, 0,
                 2, 1, 1, 4, 3, 5, 6, 3, 1, 2, 5, 2, 2, 5, 5, 5, 4, 5, 0, 5, 0,
                 0, 0, 1, 0, 5, 5, 1, 0, 2, 6, 5, 1, 1, 5, 5, 3, 1, 4, 3, 1, 0,
                 1, 1, 3, 0, 0, 5, 0, 0, 3, 0, 0, 4, 0, 3, 3, 3, 3, 0, 3, 3, 1,
                 3, 0, 2, 4, 1, 0, 0, 1, 6, 6, 4, 0, 1, 0, 4, 0, 6, 2, 3, 1, 3,
                 1, 2, 3, 2, 1, 0, 3, 6, 4, 3, 0, 4, 4, 1, 5, 0, 1, 5, 0, 6, 6,
                 4, 6, 3, 6, 6, 0, 2, 3, 1, 1, 5, 0])
        self.action_lookup_table = action_lookup_table

    def set_lookup_table(self, action_lookup_table):
        self.action_lookup_table = action_lookup_table

    def choose_action(self):
        _, situation_number = self.sense_environment()
        action_number = self.action_lookup_table[situation_number]
        return self.actions[action_number]
