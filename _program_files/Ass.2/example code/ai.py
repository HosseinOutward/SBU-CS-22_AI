import random
from time import time
from sim import Simulator, Interface
import json
import numpy as np
from queue import PriorityQueue




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
            initial_state=Simulator(sensor_data['coordinates'], sensor_data['stick_together'])
            self.predicted_actions = alg(initial_state)
            print("run time:", time()-t0)

        action = self.predicted_actions.pop()

        return action

    def heuristic(self, state):
        axs = state.coordinates.T
        # a = np.unique(axs[0]).shape[0]+\
        #     np.unique(axs[1]).shape[0]+\
        #     np.unique(axs[2]).shape[0]
        a=abs(np.unique(axs[0], return_counts=True)[1]).sum()+\
        abs(np.unique(axs[1], return_counts=True)[1]).sum()+\
        abs(np.unique(axs[2], return_counts=True)[1]).sum()
        return (a-27*3)/len(state.real_joints)

    def A_star_ramproblem(self, root_game):
        interface=Interface()

        # append the first state as (state, action_history)
        node=[root_game, [[-1,-1,-1]]]
        q_i = PriorityQueue()
        q_i.put((float('inf'), 0))
        p=[node]

        while not q_i.empty():
            # pop first element from queue
            best_i = q_i.get()[1]
            node = p[best_i]
            p[best_i]=None

            # get the list of legal actions
            actions_list = interface.valid_actions(node[0], np.transpose(node[1])[1])

            for action in actions_list:
                # copy the current state
                child_state = interface.copy_state(node[0])

                # take action and change the copied node
                interface.evolve(child_state, action)

                if not interface.valid_state(child_state): continue
                
                # add children to queue
                new_node = [child_state, [action] + node[1]]
                q_i.put((len(node[1])+self.heuristic(child_state), len(p)))
                p.append( new_node )
                
                # return if goal test is true
                if interface.goal_test(child_state): return [action] + node[1][:-1]

    def BFS_SAMPLE_CODE(self, root_game):
        interface=Interface()

        q = []
        # append the first state as (state, action_history)
        q.append([root_game, [[-1,-1,-1]]])

        while q:
            # pop first element from queue
            node = q.pop(0)

            # get the list of legal actions
            actions_list = interface.valid_actions(node[0], np.transpose(node[1])[1])

            # randomizing the order of child generation
            np.random.shuffle(actions_list)

            for action in actions_list:
                # copy the current state
                child_state = interface.copy_state(node[0])

                # take action and change the copied node
                interface.evolve(child_state, action)

                if not interface.valid_state(child_state): continue

                # add children to queue
                q.append([child_state, [action] + node[1]])

                # return if goal test is true
                if interface.goal_test(child_state):
                    return [action] + node[1][:-1]
