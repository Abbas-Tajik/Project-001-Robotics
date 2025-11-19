# Robots/bender_v1_3.py
from Robots.base_robot import BaseRobot, Feature
from Problem_Domain.action import Action
from random import choice

class Bender_V1_3(BaseRobot):
    def __init__(self, name="Bender_V1.3"):
        super().__init__(name)
        self.defeat_message_shown = False
        self.victory_message_shown = False

    def set_environment(self, environment):
        """Reset message flags for each new trial."""
        super().set_environment(environment)
        self.defeat_message_shown = False
        self.victory_message_shown = False

    def get_actions_toward_cans(self):
        """Find all actions that move toward visible cans (from CanFollowingRobot)."""
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
        Enhanced strategy combining techniques from top robots:
        can prioritisation, wall avoidance, and persistent movement.
        """
        self.sense_environment()

        # 1. If standing on a can, pick it up.
        if self.sensory_data.centre_square == Feature.can:
            return Action.pick_up_can

        # 2. If visible cans exist, move toward them (from CanFollowingRobot)
        can_actions = self.get_actions_toward_cans()
        if can_actions:
            return choice(can_actions)

        # 3. Smart exploration - avoid walls and prefer movement over staying (from CanFollowingRobot)
        safe_moves = []
        if self.sensory_data.north_square != Feature.wall:
            safe_moves.append(Action.move_north)
        if self.sensory_data.east_square != Feature.wall:
            safe_moves.append(Action.move_east)
        if self.sensory_data.south_square != Feature.wall:
            safe_moves.append(Action.move_south)
        if self.sensory_data.west_square != Feature.wall:
            safe_moves.append(Action.move_west)
        
        if safe_moves:
            return choice(safe_moves)
        else:
            # 4. Only stay put if completely surrounded by walls
            return Action.do_nothing

    def evaluate_game_end(self, environment):
        """Check if the game has ended and print appropriate message."""
        if hasattr(environment, 'count_cans'):
            cans_remaining = environment.count_cans()
            # Win if collected all cans (round ends early)
            if cans_remaining == 0 and not self.victory_message_shown:
                print(f"Woohoo, I won... Bite my shiny metal ass! (Score: {self.score})")
                self.victory_message_shown = True
                return True
        return False
    
    def evaluate_trial_end(self):
        """Print result at the end of each trial based on comparative performance."""
        if not self.victory_message_shown:
            # Based on the robot rankings, use a threshold that reflects competitive performance
            # Top robots score 350-450, so we need a realistic threshold
            if self.score > 350:  # Competitive performance (above average robots)
                print(f"Woohoo, I won... Bite my shiny metal ass! (Score: {self.score})")
            else:  # Below average performance
                print(f"Damn, I lost... My life, and by extension everyone else's, is meaningless. (Score: {self.score})")
