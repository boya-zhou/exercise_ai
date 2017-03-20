from search import astar_search, Problem, recursive_best_first_search, hill_climbing
import sys
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree

letters = 'abcdefghijklmnopqrstuvwxyz'
N = 6
nodes = list(letters[:N])
b = np.random.random_integers(0,10,size=(N,N))
b_symm = (b + b.T)/2
np.fill_diagonal(b_symm, sys.maxsize)
#costs = [[sys.maxsize, 3, 4], [3, sys.maxsize, 5], [4, 5, sys.maxsize]]
costs = b_symm

print (costs)

def list_to_string(list_):
    return '\n'.join([''.join(row) for row in list_])

class TSPProblem(Problem):

    def __init__(self, nodes, costs, initial=None, goal=None):
        self.nodes = nodes
        self.costs = costs
        self.start = self.nodes[0]
        self.initial = self.nodes[0]
        self.state = ''
        self.goal = goal

    def actions(self, state):
        # print ('state in actions: {}'.format(state))
        self.state = state
        l = list(state[1:])
            
        actions = []
        for ite in self.nodes:
            if ite not in l:
                actions.append(ite)
        if len(state) != len(nodes) and self.start in actions:
            actions.remove(self.start)
        # print ('possible actions: {}'.format(actions))
        return actions

    def result(self, state, action):
        # print ('state {}, action {} in result'.format(state, action))
        state += action
        return state

    def goal_test(self, state):
        # print ('lenght of state is {}'.format(len(state)))
        return len(state) == len(self.nodes)+1 and state[-1] == self.start

    def path_cost(self, c, state1, action, state2):
        # print ('state1 in path_cost {}\t state2 {}'.format(state1, state2))
        return c+self.costs[self.nodes.index(state1[-1])][self.nodes.index(action)]

    def h(self, node):
        # use MST as h funnction
        current_state = node.state
        cs_list = list(current_state)
        # print('current_state in h {}'.format(cs_list))
        last_node = cs_list[-1]
        last_node_idx = self.nodes.index(last_node)
        rest_nodes = [x for x in self.nodes if x not in cs_list]
        if len(rest_nodes) == 0:
            return 0
        shortest_cost = self.costs[last_node_idx][self.nodes.index(rest_nodes[0])]
        for ite in rest_nodes:
            cost = self.costs[last_node_idx][self.nodes.index(ite)]
            if shortest_cost > cost:
                shortest_cost = cost
        # shortest path from starter
        shortest_cost_starter = self.costs[0][self.nodes.index(rest_nodes[0])]
        for ite in rest_nodes:
            cost = self.costs[0][self.nodes.index(ite)]
            if shortest_cost > cost:
                shortest_cost_starter = cost
        cs_idx_list = [self.nodes.index(x) for x in cs_list]
        
        mst_matrix = np.delete(self.costs, cs_idx_list, 0)
        mst_matrix = np.delete(mst_matrix, cs_idx_list, 1)
        X = csr_matrix(mst_matrix)
        Tcsr = minimum_spanning_tree(X)
        tcsr_matrix = Tcsr.toarray().astype(int)
        mst_cost_sum = np.sum(tcsr_matrix)
        return mst_cost_sum+shortest_cost+shortest_cost_starter

    def value(self, state):
        # print('state in value: {} \t initial: {}'.format(state, self.initial))
        return -1*self.costs[self.nodes.index(self.state[-1])][self.nodes.index(state[-1])]
        #return len(self.state) - len(self.nodes)

# result = astar_search(TSPProblem(nodes, costs))
result = recursive_best_first_search(TSPProblem(nodes, costs))
step_count = 0

#print(result)
for action in result.path():
    print ('\nMove {}'.format(action.action))
    print (action.state)
    step_count += 1
print('total steps is {}'.format(step_count))
