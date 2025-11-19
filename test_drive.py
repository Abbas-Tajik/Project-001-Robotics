"""
This script lets you test a simple simulated robot
in a randomly generated environment.

Import whichever robot you want to test drive.
"""
import os
import time
from colorama import init, Back
from Problem_Domain.environment import Environment

# from Robots.base_robot import BaseRobot as Robot
# from Robots.sensing_robot import SensingRobot as Robot
# from Robots.smarter_sensing_robot import SmarterSensingRobot as Robot
# from Robots.can_following_robot import CanFollowingRobot as Robot
# from Robots.experimental_robot import ExperimentalRobot as Robot
# from Robots.lookup_table_robot import LookupTableRobot as Robot
# from Reinforcement_Learning.train_q_learner import get_trained_q_learning_robot as Robot
from Reinforcement_Learning.train_q_learner import get_trained_q_learning_robot_optimized as Robot


ROBOT = Robot('Robot under test')
NUMBER_OF_ACTIONS = 200
REDRAW_DELAY = 0.2
REWARD_WINDOW_LENGTH = 40
ENVIRONMENT = Environment(record_rewards=True)


init(autoreset=True)
env_colour_map = {
    0: Back.BLACK + '  ',
    1: Back.BLACK + '🥫',
    3: Back.BLACK + '🤖',
    4: Back.BLUE + '🤖',
}

reward_colour_map = {
    -5: Back.RED + '  ',
    -1: Back.MAGENTA + '  ',
    0: Back.BLACK + '  ',
    10: Back.GREEN + '  ',
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_environment():
    for row in ENVIRONMENT.printable_grid():
        print(''.join(env_colour_map[val] for val in row))


def display(step, action):
    clear_screen()
    display_environment()
    print(f'Cans: {ENVIRONMENT.count_cans()}')
    print(f'Score: {ROBOT.score}')
    print(f'Reward: {ENVIRONMENT.reward}')
    print(f'Rewards: {''.join(reward_colour_map[val] \
                              for val in ENVIRONMENT.recent_rewards(REWARD_WINDOW_LENGTH))}')
    print(f'Time step: {step}')
    print(action)


# Ramdomise the environment with the current time to get a different environment each time.
ENVIRONMENT.randomise(time.time())
ROBOT.set_environment(ENVIRONMENT)
ENVIRONMENT.set_robot(ROBOT)
clear_screen()
display_environment()

for i in range(NUMBER_OF_ACTIONS):
    action = ROBOT.choose_action()
    ENVIRONMENT.perform_action(action)
    display(i, action)
    time.sleep(REDRAW_DELAY)
    if ENVIRONMENT.count_cans() == 0:
        break
