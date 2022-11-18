from ai import *
from sim import *
from gui import *


def main(sample_input_json):
    game = Simulator(sample_input_json['coordinates'], sample_input_json['stick_together'])
    interface = Interface()
    agent = Agent()
    gui = Graphics()

    action_count = 0
    print("initial map")
    gui.display(game)
    while not (interface.goal_test(game)):
        action = agent.act(interface.perceive(game))

        print("attempting", action)
        interface.evolve(game, action)
        gui.display(game)
        if not interface.valid_state(game): raise 'reached invalid state'
        print("\n")
        action_count += 1

    print(
        "\n\nпобеда!!!",
        "\nyour cost (number of actions):", action_count,
        '\n\ncurrent map state:'
    )
    gui.display(game)


if __name__ == "__main__":
    with open(r"problem_set.txt", 'r') as fp:
        res=eval(fp.read())
    main(res[0])
