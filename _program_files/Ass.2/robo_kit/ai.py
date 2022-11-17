import random
from time import time
import json


# *** you can change everything except the name of the class, the act function and the sensor_data ***


class Agent:
    # ^^^ DO NOT change the name of the class ***

    def __init__(self):
        pass

    # the act function takes a json string as input
    # and outputs an action string
    # ('U' is go up,   'L' is go left,   'R' is go right,   'D' is go down,  'C' is clean tile)
    def act(self, percept):
        # ^^^ DO NOT change the act function above ***

        sensor_data = json.loads(percept)
        # ^^^ DO NOT change the sensor_data above ***

        # TODO implement your agent here

        return action
