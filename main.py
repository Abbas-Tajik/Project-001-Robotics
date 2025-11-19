"""
Compare all of our robots across a consistent set of randomly generated environments. 
"""

from random import randint, seed
from Problem_Domain.environment import Environment
from Robots.base_robot import BaseRobot
from Robots.sensing_robot import SensingRobot
from Robots.smarter_sensing_robot import SmarterSensingRobot
from Robots.can_following_robot import CanFollowingRobot
from Robots.experimental_robot import ExperimentalRobot
from Robots.lookup_table_robot import LookupTableRobot
from Reinforcement_Learning.train_q_learner import get_trained_q_learning_robot
from Reinforcement_Learning.train_q_learner import get_trained_q_learning_robot_optimized
from Robots.Bender_V1_3 import Bender_V1_3

seed(0)  # Set an seed initial value if we want reproducable results.

NUMBER_OF_ACTIONS = 200
NUMBER_OF_TRIALS = 10  # Perfect for showcasing Bender's humor

# Create a list of random seeds, one for each trial, to ensure that each robot gets
# the same set of randomly generated environments. This will be true even if we don't
# set the initial seed, although in that case it will be a different set of randomly
# generated environments in each run.
ENVIRONMENT_SEEDS = [randint(-2147483648, 2147483647)
                     for _ in range(NUMBER_OF_TRIALS)]


def evaluate_robot(robot):
    """
    Evaluate a single robot and return the average score across all trials.
    """
    total_score = 0
    for environment_seed in ENVIRONMENT_SEEDS:
        environment = Environment(random_seed=environment_seed)
        robot.set_environment(environment)
        environment.set_robot(robot)
        for _ in range(NUMBER_OF_ACTIONS):
            environment.perform_action(robot.choose_action())
            # Check for Bender's game end conditions
            if hasattr(robot, 'evaluate_game_end'):
                robot.evaluate_game_end(environment)
        
        # Check for Bender's trial end result if no victory message was shown
        if hasattr(robot, 'evaluate_trial_end'):
            robot.evaluate_trial_end()
            
        total_score += robot.score
    print(f'Average score for {robot.name}: {total_score / NUMBER_OF_TRIALS}')


def evaluate_all_robots(robots_under_test):
    """
    Evaluate each robot in turn.
    """
    for robot in robots_under_test:
        evaluate_robot(robot)


if __name__ == '__main__':
    # Uncomment the line below to test ONLY Bender
    # robots = [Bender_V1_2('Bender_V1.2')]
    
    # Comment out the line below to test only Bender
    robots = [
        BaseRobot('Random Robby'),
        SensingRobot('Sensing Sadie'),
        SmarterSensingRobot('Smarter Sally'),
        CanFollowingRobot('Magnetic Morag'),
        ExperimentalRobot('Experimental Eddie'),
        LookupTableRobot('Evolved Eva'),
        get_trained_q_learning_robot('Quentin the Q-Learner'),
        get_trained_q_learning_robot_optimized('Optimus Q'),
        Bender_V1_3('Bender_V1.3')
    ]
    evaluate_all_robots(robots)
