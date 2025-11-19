"""
A hand-crafted robot controller that tries to improve on the can following robot.
"""

from Robots.can_following_robot import CanFollowingRobot, Feature, Action


class ExperimentalRobot(CanFollowingRobot):
    """
    Based on the CanFollowingRobot but prefers to walk towards the end of a chain of cans and then
    pick them up on the way back.
    """
    def choose_action(self):
        action = CanFollowingRobot.choose_action(self)

        # Favour actions that walk towards the end of a chain of cans so that the robot can follow
        # it back.
        # Follow the chain of cans north or west so that the robot tends away from the starting
        # point (the northwest corner) when it picks them up on the way back.
        # This is based on the intuition that the robot will have already spent time near the
        # starting point and so there are likely to be fewer cans around there.
        if self.sensory_data.north_square == Feature.can \
            and self.sensory_data.centre_square == Feature.can:
            action = Action.move_north
        if self.sensory_data.west_square == Feature.can \
            and self.sensory_data.centre_square == Feature.can:
            action = Action.move_west

        return action
