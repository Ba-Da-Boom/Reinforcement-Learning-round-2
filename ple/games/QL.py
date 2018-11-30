import numpy as np


class Intelligent_neural_network:
    ''' qlearning algorithm
    1. We sample it
    2. We observed the reward and the next state
    3. We take action with the highest Q

    thanks to the medium post https://medium.com/@jonathan_hui/rl-introduction-to-deep-reinforcement-learning-35c25e04c199
    thanks to the video https://www.youtube.com/watch?v=MQ6pP65o7OM
    '''

    def __init__(self, actions):
        ''' some caracteristics for our model

        alpha is the learning rate
        epsilon is the discount factor

        '''

        self.actions = actions
        self.alpha = 0.2
        self.epsilon = 0.1
        self.gamma = 0.9
        self.memory = []
        self.q = {}

    def model(self, state, action):
        ''' basic model
            state : key
            action : key
            return : dict

        '''
        return self.q.get((state, action), 0.0)


    def observation(self, state_1,state_2, reward, actions):
        ''' osbserve the model and learn about it

            state_1 : float
            state_2 : float
            reward  : float
            actions : float
            return : float

         '''

        if state_1 and actions not in self.q:
            update = reward
            self.q[(state_1, actions)] = update
        else:
            max_q = max(self.model(state_2, action)for action in self.actions)
            valueq = reward + self.gamma * max_q
            update = (self.alpha) * (self.q[(state_1,actions)] - valueq)
            self.q[(state_1, actions)] += update

        return update


    def chooseAction(self, state, observation):
        ''' chose an action amongs the other
            state : key
            return : key
        '''
        explo = np.random.random()

        if explo < self.epsilon :
            action = np.random.choice(self.actions)

        else:
            one_q = [self.model(state, action) for action in self.actions]
            max_q = max(one_q)

            count_q = one_q.count(max_q)
            if count_q > 1.0:
                best_q=[i for i in range(len(self.actions)) if one_q[i] ==max_q]
                chose = np.random.choice(best_q)
            else:
                chose = one_q.index(max_q)
            action = self.actions[chose]
        return action

