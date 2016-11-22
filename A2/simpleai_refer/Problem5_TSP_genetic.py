from traditional import *
from utils import *
from local import *
import sys
import numpy as np

letters = 'abcdefghijklmnopqrstuvwxyz'
N = 6
nodes = list(letters[:N])
b = np.random.random_integers(0,10,size=(N,N))
b_symm = (b + b.T)/2
np.fill_diagonal(b_symm, sys.maxsize)
#costs = [[sys.maxsize, 3, 4], [3, sys.maxsize, 5], [4, 5, sys.maxsize]]
costs = b_symm

def list_to_string(list_):
    return ''.join(list_)

initial = ''
for ite in nodes:
    initial += ite
initial += nodes[0]

class TSPProblem(SearchProblem):

    def __init__(self, nodes, costs, initial=None):
        self.node_size = len(nodes)
        self.nodes = nodes
        self.costs = costs
        self.start = self.nodes[0]
        self.initial = initial
        self.initial_state = initial

    def actions(self, state):
        #print('state in actions {}'.format(state))
        # swapping the second town with some other town
        if len(state) <= 3:
            return []
        l = list(state)
        second = l[1]
        actions = []
        for i in range(2, len(state)-1):
            l[1] = l[i]
            l[i] = second
            action = list_to_string(l)
            l[i] = l[1]
            l[1] = second
            actions.append(action)
        return actions

    def result(self, state, action):
        #print('state in result {} \t action in result {}'.format(state, action))

        state = action
        return state

    def cost(self, c, state1, action, state2):
        return c+1

    def value(self, state):
        #print ('state in value {}'.format(state))
        l = list(state)
        cost = 0
        for i in range(0, len(l)-1):
            index_1 = self.nodes.index(l[i])
            index_2 = self.nodes.index(l[i+1])
            cost += self.costs[index_1][index_2]
        if cost == 0:
            return sys.maxsize
        else:
            return 1/cost

    # partially mapped crossover
    def crossover(self, state1, state2):
        tmp1 = list(state1)
        tmp2 = list(state2)
        half_size = self.node_size / 2
        idx_1 = np.random.randint(1, half_size)
        idx_2 = np.random.randint(half_size, self.node_size)
        first_part_1 = tmp1[:idx_1]
        third_part_1 = tmp1[idx_2:]
        mid_part_1 = tmp1[idx_1:idx_2]
        first_part_2 = tmp2[:idx_1]
        third_part_2 = tmp2[idx_2:]
        mid_part_2 = tmp2[idx_1:idx_2]
        
        # get the elements mapping
        mapping1 = {}
        for i in range(idx_1, idx_2):
            mapping1[tmp1[i]] = tmp2[i]
        mapping2 = {}
        for i in range(idx_1, idx_2):
            mapping2[tmp2[i]] = tmp1[i]
        # check duplicates
        tmp_first_part = []
        for ite in first_part_1:
            while ite in mid_part_2:
                ite = mapping1[ite]
            tmp_first_part.append(ite)
        tmp_third_part = []
        for ite in third_part_1:
            while ite in mid_part_2:
                ite = mapping1[ite]
            tmp_third_part.append(ite)
        off1 = tmp_first_part + mid_part_2 + tmp_third_part
        # off2
        tmp_first_part = []
        for ite in first_part_2:
            while ite in mid_part_1:
                ite = mapping2[ite]
            tmp_first_part.append(ite)
        tmp_third_part = []
        for ite in third_part_2:
            while ite in mid_part_1:
                ite = mapping1[ite]
            tmp_third_part.append(ite)
        off2 = tmp_first_part + mid_part_2 + tmp_third_part

        return list_to_string(off1)

    def mutate(self, state):
        tmp = list(state)
        idx_1 = np.random.randint(1, self.node_size)
        idx_2 = np.random.randint(1, self.node_size)
        tmp[idx_1], tmp[idx_2] = tmp[idx_2], tmp[idx_1]
        return list_to_string(tmp)

    def generate_random_state(self):
        state = self.nodes[0]
        tmp = self.nodes[1:]
        np.random.shuffle(tmp)
        for ite in tmp:
            state += ite
        state += self.nodes[0]
        return state

result = genetic(TSPProblem(nodes, costs, initial))
print (result.path())
