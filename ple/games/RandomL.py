#! /usr/bin/env python3

import numpy as np


class Dumb_neural_network():
    ''' reinforcement agent '''

    def __init__(self, actions):
        self.actions = actions

    def pickactions(self, actions, obs):
        return self.actions[np.random.randint(0, len(self.actions))]


