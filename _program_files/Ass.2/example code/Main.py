from ai import *
from sim import *
from gui import *


sample_input_json={
    "coordinates": [
        [-5,2, -6],
        [-5,2, -5],
        [-5,2, -4],
        [-4,2, -4],
        [-3,2, -4],
        [-3,2, -3],
        [-3,2, -2],
        [-2,2, -2],
        [-1,2, -2],
        [-1,2, -1],
        [0, 2, -1],
        [0, 2,  0],
        [0, 1,  0],
        [0, 0,  0],
        [1, 0,  0],
        [2, 0,  0],
        [2, 0,  1],
        [3, 0,  1],
        [3, 0,  2],
        [3, 0,  3],
        [4, 0,  3],
        [4, 0,  4],
        [4, 0,  5],
        [5, 0,  5],
        [5, 0,  6],
        [6, 0,  6],
        [7, 0,  6]
    ],
    "stick_together": [
        [5, 6],
        [12, 13],
        [14, 15],
        [15, 16],
        [18, 19]
    ]
}


def main():
    game = Simulator(sample_input_json['coordinates'], sample_input_json['stick_together'])
    interface=Interface()
    agent = Agent()
    gui = Graphics()

    action_count=0
    print("initial map")
    # gui.display(game)
    while not (interface.goal_test(game)):
        action = agent.act(interface.perceive(game))
        
        print("attempting", action)
        interface.evolve(game, action)
        if not interface.valid_state(game): raise 'reached invalid state'
        # gui.display(game)
        print("\n")
        action_count+=1

    print(
        "\n\nпобеда!!!",
        "\nyour cost (number of actions):", action_count,
        '\n\ncurrent map state:'
    )
    gui.display(game)


if __name__ == "__main__":
    main()