from search import Problem, hill_climbing
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

class TSPProblem(Problem):

    def __init__(self, nodes, costs, initial=None, goal=None):
        self.nodes = nodes
        self.costs = costs
        self.start = self.nodes[0]
        self.initial = initial
        self.state = ''
        self.goal = goal

    def actions(self, state):
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
        state = action
        return state

    def path_cost(self, c, state1, action, state2):
        return c+1

    def value(self, state):
        l = list(state)
        cost = 0
        for i in range(0, len(l)-1):
            index_1 = self.nodes.index(l[i])
            index_2 = self.nodes.index(l[i+1])
            cost += -1 * self.costs[index_1][index_2]
        return cost

#result = astar_search(TSPProblem(nodes, costs))
#result = recursive_best_first_search(TSPProblem(nodes, costs))
result = hill_climbing(TSPProblem(nodes, costs, initial))
print(['-'.join(list(result))])
