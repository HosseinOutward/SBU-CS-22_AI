import sys

from agent_files.ai import *
from eval_env import *


def test_one_problemset(sample_input_json):
    game = Simulator(sample_input_json['coordinates'], sample_input_json['stick_together'])
    interface = Interface()
    agent = Agent()

    action_count = 0
    while not (interface.goal_test(game)):
        action = agent.act(interface.perceive(game))
        interface.evolve(game, action)
        if not interface.valid_state(game): raise 'reached invalid state'
        action_count += 1
    return action_count


with open(r"problem_set.txt", 'r') as fp: res=eval(fp.read())
cost=test_one_problemset(res[int(sys.argv[1])])
print('\n','\n')
print(cost)