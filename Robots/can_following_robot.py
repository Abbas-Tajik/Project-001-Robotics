from Robots.smarter_sensing_robot import SmarterSensingRobot, Feature, Action
from random import choice


class CanFollowingRobot(SmarterSensingRobot):
    """
    Pick up a can if possible, otherwise walk towards a can if one can be seen.
    """
    def get_default_action(self):
        """
        Use the SmarterSensingRobot to get the default action,
        but don't accept the do nothing action.
        """
        default_action = SmarterSensingRobot.choose_action(self)
        while default_action == Action.do_nothing:
            default_action = SmarterSensingRobot.choose_action(self)
        return default_action

    def get_actions_that_move_towards_a_can(self):
        """
        Find all the actions that move towards a can.
        """
        actions = []
        if self.sensory_data.north_square == Feature.can:
            actions.append(Action.move_north)
        if self.sensory_data.east_square == Feature.can:
            actions.append(Action.move_east)
        if self.sensory_data.south_square == Feature.can:
            actions.append(Action.move_south)
        if self.sensory_data.west_square == Feature.can:
            actions.append(Action.move_west)
        return actions

    def choose_action(self):
        """
        Returns:
        - The action to pick up a can if possible,
        - otherwise an action that walks towards a can if one can be seen,
        - otherwise an action chosen by the base class.
        """
        default_action = self.get_default_action()
        if default_action == Action.pick_up_can:
            return default_action

        alternative_actions = self.get_actions_that_move_towards_a_can()
        if alternative_actions:
            return choice(alternative_actions)

        return default_action
