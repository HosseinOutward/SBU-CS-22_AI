import random
from copy import deepcopy


class Simulator:
    def __init__(self, map, agent_loc):
        self.map = map
        self.agent_loc = agent_loc
    
    def take_action(self, action):
        # TODO implement the game logic here. change map and agent_loc according to the action
