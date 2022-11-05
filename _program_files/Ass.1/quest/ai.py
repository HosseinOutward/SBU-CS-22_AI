import random
from time import time
from sim import *
import json

class Agent:
    def __init__(self, interface):
        self.interface = interface
        self.predicted_actions = []

    def act(self, state):
        json_sensor_data = json.loads(self.interface.perceive(state))
        alg = self.BFS_SAMPLE_CODE
    
        if self.predicted_actions == []:
            t0=time()
            initial_state=Simulator(json_sensor_data['map'], json_sensor_data['location'])
            self.predicted_actions = alg(initial_state)
            print("run time:", time()-t0)

        action = self.predicted_actions.pop()

        return action

    def BFS_SAMPLE_CODE(self, root_game):
        q = []
        # append the first state as (state, action_history)
        q.append([root_game, []])

        while q:
            # pop first element from queue
            node = q.pop(0)
            
            # get the list of legal actions
            actions_list = self.interface.valid_actions(node)
            
            # randomizing the order of child generation
            random.shuffle(actions_list)
            
            for action in actions_list:
                # copy the current state
                child_state = self.interface.copy_state(node[0])
                
                # take action and change the copied node
                self.interface.evolve(child_state, action)
                
                # add children to queue
                q.append([child_state, [action] + node[1]])
                
                # return if goal test is true
                if self.interface.goal_test(child_state): return [action] + node[1]


class Interface:
    def __init__(self):
        pass

    # an example for what this class is supposed to do
    # here, it will make sure the action that is being
    # requested is in a correct format. this func won't return anything
    # the actual simulator must only deal with the game logic and nothing more
    def evolve(self, state, action):
        if type(action) is not str: raise("action is not a string")
        action=action.upper()
        if action not in self.valid_actions(state): raise("action is not valid")
        state.take_action(action)

    # another example for what this class is supposed to do
    # note that the variables like map and agent_loc are references
    # meaning changing the copied state will also change the original state
    # to copy the actual data, you must use something like deepcopy
    # note that deepcopy is not perfect and is both slow and might not fully copy everything
    # it recommended to use a custom copy function that copies all and only the data that is needed
    def copy_state(self, state):
        _copy = Simulator(None,None)
        _copy.map = deepcopy(state.map)
        _copy.agent_loc = deepcopy(state.agent_loc)
        return _copy

    def perceive(self, state):
        # TODO return what the agent will see ('map' and 'location') as json string
        # help --> json.dumps({'map':??, 'location':??})

    def goal_test(self, state):
        # TODO return if goal has been reached

    def valid_actions(self, state):
        # TODO return list of legal actions

