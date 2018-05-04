import numpy as np
import matplotlib.pyplot as plt


"""
Similar to any reinforcemnet learning there are three main questions that we need to answer:

1. what is an state: The state is defined as pair of (number of cars remained in first location, number of cars remained in second location). Clearly the state space is (0,0) to (20,20)
action space. Action is defined as number of cars transfer from location 1 to location 

2. Action space is an integer number between -5 to 5 shows number of cars moved from location 1 to location 2. 
   Negative number is reverse flow from 2nd location 2 to 1st location.

3.Environment: Given a space and an action, environment defines reward and next state. 

4. transition probability

"""



class State(object):
    NUM_CARS = 20
    def __init__(self, n1, n2):
        self.n_loc1 = min(max(n1, 0), self.NUM_CARS)
        self.n_loc2 = min(max(n2, 0), self.NUM_CARS)

    def get_n_loc1(self):
        return self.n_loc1

    def get_n_loc2(self):
        return self.n_loc2

    def __str__(self):
        return "(" + str(self.n_loc1) + "," + str(self.n_loc2) + ")"


class Env(object):
    ACTION_COST = 2
    REQUEST_LOC1 = 3
    REQUEST_LOC2 = 4

    RETURN_LOC1 = 3
    RETURN_LOC2 = 2

    def __init__(self):
        self.state = State(20, 20)

    def reset(self):
        self.state = State(20, 20)

    def step(self, action):
        """
        :param action: int number between -5 and 5. It shows number of cars moved from loc1 to loc2
        @return: 1. reward for taking the action. Reward is a non-negative number
                 2. next state.
        """
        act = action
        cost = abs(act) * self.ACTION_COST

        num_return_loc1 = np.random.poisson(lam=self.RETURN_LOC1)
        num_return_loc2 = np.random.poisson(lam=self.RETURN_LOC2)

        if act > 0:
            total_car_loc1 = self.state.get_n_loc1() + num_return_loc1
            if act > total_car_loc1:
                act = total_car_loc1
            total_car_loc1 = max(0, min(total_car_loc1 - act, State.NUM_CARS))

            total_car_loc2 = self.state.get_n_loc2() + num_return_loc2 + act
            total_car_loc2 = min(total_car_loc2, State.NUM_CARS)
        else:
            total_car_loc2 = self.state.get_n_loc2() + num_return_loc2
            if abs(act) > total_car_loc2:
                act = -1 * total_car_loc2
            total_car_loc2 = max(0, min(total_car_loc2 + act, State.NUM_CARS))

            total_car_loc1 = self.state.get_n_loc1() + num_return_loc1 - act
            total_car_loc1 = min(total_car_loc1, State.NUM_CARS)

        num_request_loc1 = np.random.poisson(lam=self.REQUEST_LOC1)
        num_request_loc1 = min(num_request_loc1, total_car_loc1)

        num_request_loc2 = np.random.poisson(lam=self.REQUEST_LOC2)
        num_request_loc2 = min(num_request_loc2, total_car_loc2)

        num_remain_loc1 = total_car_loc1 - num_request_loc1
        num_remain_loc2 = total_car_loc2 - num_request_loc2

        reward = (num_request_loc2 + num_request_loc1) * 10 - cost

        self.state = State(num_remain_loc1, num_remain_loc2)

        return reward, self.state

    def get_state(self):
        return self.state


def select_action(q):
    if np.sum(q) == 0:
        qq = [1.0/len(q) for _ in q]
    else:
        qq = [x/np.sum(q) for x in q]
    r = np.random.uniform(0, 1)
    for i in range(len(qq)):
        if np.sum(qq[:i+1]) > r:
            return i


class Run(object):

    env = Env()
    lr = .01
    gamma = .9
    epsilon = .1
    Q = np.zeros([20, 20, 11])

    a = []
    b = []
    myreward = []


    def run(self):
        for episode in range(100000):
            self.env.reset()
            for j in range(500):
                s = self.env.get_state()
                if self.epsilon*1.0/(episode+1) < np.random.uniform(0, 1):
                    action = np.random.randint(-5, 6)
                else:
                    #action = np.argmax(Q[s.n_loc1-1][s.n_loc2-1]) - 5
                    action = select_action(self.Q[s.n_loc1-1][s.n_loc2-1]) - 5

                rew, new_s = self.env.step(action)

                v_s_1 = max(self.Q[new_s.n_loc1 - 1, new_s.n_loc2 - 1])

                self.Q[s.n_loc1 - 1, s.n_loc2 - 1, action + 5] = self.Q[s.n_loc1-1, s.n_loc2-1, action + 5] + \
                                                            self.lr * (rew + self.gamma*v_s_1 - self.Q[s.n_loc1-1, s.n_loc2-1, action + 5])

            self.a.append(np.argmax(self.Q[0][19]) - 5)
            self.b.append(np.argmax(self.Q[19][0]) - 5)
            if s.n_loc1 == 19 and s.n_loc2 == 0:
                self.myreward.append(self.Q[19][0])

run = Run()
run.run()
# print run.a
# print run.b
# print run.myreward

policy = np.zeros([20, 20])
for i in range(len(run.Q)):
    for j in range(len(run.Q)):
        policy[i][j] = np.argmax(run.Q[i][j])*1.0/11.0

plt.imshow(policy, cmap='hot', interpolation='nearest')

plt.savefig('test2.png')

# for i in range(20):
#     for j in range(20):
#         print i, j, np.argmax(Q[i][j]) - 5

# print np.argmax(Q[0][9]) - 5
# print np.argmax(Q[19][0]) - 5
# print np.argmax(Q[9][0]) - 5
