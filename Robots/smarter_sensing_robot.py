from Robots.base_robot import BaseRobot, Feature, Action


class SmarterSensingRobot(BaseRobot):
    def choose_action(self):
        # Calling sense_environment will set the five sensory data:
        #   centre_square, north_square, east_square, south_square and west_square.
        # Each square can have one of the following three possible values:
        #   Feature.can, Feature.Wall and Feature.empty.
        self.sense_environment()

        # Calling choose_action in BaseRobot gets a random default action from the set of available actions.
        # Possible values are:
        #   Action.pick_up_can, Action.move_north, Action.move_south, Action.move_west,
        #   Action.move_east, Action.move_random or Action.do_nothing
        action = BaseRobot.choose_action(self)

        # Replace the randomly selected action with a new one if the robot can pick up a can
        # or if following the action means that the robot will obviously walk into a wall.
        # Also be careful to avoid moving at random next to a wall
        # and don't try to pick up a can if one hasn't been detected.
        if self.sensory_data.centre_square == Feature.can:
            action = Action.pick_up_can
        else:
            while (
                self.sensory_data.north_square == Feature.wall \
                    and action in [Action.move_north, Action.move_random] or \
                self.sensory_data.west_square == Feature.wall \
                    and action in [Action.move_west, Action.move_random] or \
                self.sensory_data.east_square == Feature.wall \
                    and action in [Action.move_east, Action.move_random] or \
                self.sensory_data.south_square == Feature.wall \
                    and action in [Action.move_south, Action.move_random] or \
                self.sensory_data.centre_square != Feature.can and action == Action.pick_up_can):
                action = BaseRobot.choose_action(self)

        # An earlier attempt that still managed to walk into walls:
        # if self.sensory_data.centre_square == Feature.can:
        #     action = Action.pick_up_can
        # elif self.sensory_data.north_square == Feature.wall:
        #     while action == Action.move_north or action == Action.move_random or action == Action.pick_up_can:
        #         action = BaseRobot.choose_action(self)
        # elif self.sensory_data.west_square == Feature.wall:
        #     while action == Action.move_west or action == Action.move_random or action == Action.pick_up_can:
        #         action = BaseRobot.choose_action(self)
        # elif self.sensory_data.east_square == Feature.wall:
        #     while action == Action.move_east or action == Action.move_random or action == Action.pick_up_can:
        #         action = BaseRobot.choose_action(self)
        # elif self.sensory_data.south_square == Feature.wall:
        #     while action == Action.move_south or action == Action.move_random or action == Action.pick_up_can:
        #         action = BaseRobot.choose_action(self)

        return action
