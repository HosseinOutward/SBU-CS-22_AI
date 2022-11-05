import random
from time import time
import json
from sim import Simulator, Interface


class Agent:
    def __init__(self, precieve_func):
        # *** DO NOT CHANGE THE precieve_func ***
        self.precieve_func = precieve_func
        # *** DO NOT CHANGE THE precieve_func ***

        self.predicted_actions = []

    def act(self, state):
        # *** DO NOT CHANGE THE json_sensor_data ***
        json_sensor_data = json.loads(self.precieve_func(state))
        # *** DO NOT CHANGE THE json_sensor_data ***

        alg = self.BFS_SAMPLE_CODE
    
        if self.predicted_actions == []:
            t0=time()
            initial_state=Simulator(json_sensor_data['map'], json_sensor_data['location'])
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
