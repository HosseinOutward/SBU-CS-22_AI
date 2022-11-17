import random
from time import time
from sim import Simulator, Interface
import json


# *** you can change everything except the name of the class, the act function and the sensor_data ***


class Agent:
    # ^^^ DO NOT change the name of the class ***

    def __init__(self):
        self.predicted_actions = []

    # the act function takes a json string as input
    # and outputs an action string
    # ('U' is go up,   'L' is go left,   'R' is go right,   'D' is go down,  'C' is clean tile)
    def act(self, percept):
        # ^^^ DO NOT change the act function above ***

        sensor_data = json.loads(percept)
        # ^^^ DO NOT change the sensor_data above ***

        alg = self.BFS_SAMPLE_CODE
    
        if self.predicted_actions == []:
            t0=time()
            initial_state=Simulator(sensor_data['map'], sensor_data['location'])
            self.predicted_actions = alg(initial_state)
            print("run time:", time()-t0)

        action = self.predicted_actions.pop()

        return action

    def BFS_SAMPLE_CODE(self, root_game):
        interface=Interface()

        q = []
        # append the first state as (state, action_history)
        q.append([root_game, []])

        while q:
            # pop first element from queue
            node = q.pop(0)
            
            # get the list of legal actions
            actions_list = interface.valid_actions(node)
            
            # randomizing the order of child generation
            random.shuffle(actions_list)
            
            for action in actions_list:
                # copy the current state
                child_state = interface.copy_state(node[0])
                
                # take action and change the copied node
                interface.evolve(child_state, action)
                
                # add children to queue
                q.append([child_state, [action] + node[1]])
                
                # return if goal test is true
                if interface.goal_test(child_state): return [action] + node[1]
