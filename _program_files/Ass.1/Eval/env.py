from copy import deepcopy
import json


class Env:
    def __init__(self, map, agent_loc):
        self.map = map
        self.agent_loc = agent_loc

    def take_action(self, action):
        # TODO implement the game logic here
        if action == 'C':
            self.map[self.agent_loc[0]][self.agent_loc[1]] = 0
            return

        delta_i, delta_j = {"U": (-1, 0), "D": (+1, 0), "R": (0, +1), "L": (0, -1)}[action]

        i, j = self.agent_loc
        new_i, new_j = max(0, min(len(self.map) - 1, i + delta_i)), max(0, min(len(self.map[0]) - 1, j + delta_j))

        if self.map[new_i][new_j] == -1:
            return

        self.agent_loc = [new_i, new_j]

    def evolve(self, action):
        if type(action) is not str: raise ("action is not a string")
        action = action.upper()
        if action not in self.valid_actions(): raise ("action is not valid")
        self.take_action(action)

    def perceive(self):
        # TODO return what the agent will see ('map' and 'location') as json
        return json.dumps({"map": self.map, "location": self.agent_loc})

    def goal_test(self):
        # TODO return if goal has been reached
        for row in self.map:
            if row.count(1) != 0: return False
        return True

    def valid_actions(self):
        # TODO return list of legal actions
        return ["U", "L", "R", "D", "C"]
