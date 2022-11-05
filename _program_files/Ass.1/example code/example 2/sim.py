from copy import deepcopy
import json


class Simulator:
    def __init__(self, map, agent_loc):
        self.map = map
        self.agent_loc = agent_loc
    
    def take_action(self, action):
        # TODO implement the game logic here
        if action == 'C':
            self.map[self.agent_loc[0]][self.agent_loc[1]] = 0
            return

        delta_i, delta_j = {"U": (-1,0), "D": (+1,0), "R": (0,+1), "L": (0,-1)}[action]

        i,j=self.agent_loc
        new_i, new_j=max(0,min(len(self.map)-1, i+delta_i)), max(0,min(len(self.map[0])-1, j+delta_j))

        if self.map[new_i][new_j] == -1:
            return

        self.agent_loc = [new_i, new_j]


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
        # TODO return what the agent will see ('map' and 'location') as json
        return json.dumps({"map":state.map, "location":state.agent_loc})

    def goal_test(self, state):
        # TODO return if goal has been reached
        for row in state.map:
            if row.count(1) != 0: return False
        return True

    def valid_actions(self, state):
        # TODO return list of legal actions
        return ["U","L","R","D","C"]

