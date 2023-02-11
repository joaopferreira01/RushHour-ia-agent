# Module: tree_search
# 
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2019,
#  Inteligência Artificial, 2014-2019

from abc import ABC, abstractmethod
import copy

import time

# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial):
        self.domain = domain
        self.initial = initial
    def goal_test(self,state):
        return self.domain.satisfies(state)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state,parent, action=None, cost = 0, heuristic = 8): 
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic

    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self.state)

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        root = SearchNode(problem.initial, None)
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        #self.explored_states = []

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.action]
        path = self.get_path(node.parent)
        path += [node.action]
        return(path)

    # procurar a solucao
    def search(self):
        explored_states = set()
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
        
            if self.problem.goal_test(node.state):
                self.solution = node
                # print("----soluçao encontrada-----")
                return self.get_path(node)

            lnewnodes = []
            #print(self.problem.domain.actions(node.state))

            for a in self.problem.domain.actions(node.state):
                # st = time.time()
                auxstate = copy.deepcopy(node.state)
                newstate = self.problem.domain.result(auxstate,a)
                # ft = time.time()
                # print("tempo copia de estaado e result:", ft-st)
                
                if newstate.grid != node.state.grid and str(newstate) not in explored_states:
                    # print(newstate)
                    explored_states.add(str(newstate))
                    newnode = SearchNode(
                        newstate,
                        node,
                        a,
                        node.cost + self.problem.domain.cost(),
                        self.problem.domain.heuristic(newstate))
                    lnewnodes.append(newnode)

            self.add_to_open(lnewnodes)
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            self.open_nodes = sorted(self.open_nodes + lnewnodes, key = lambda node: node.cost)
        elif self.strategy == 'greedy':
            self.open_nodes = sorted(self.open_nodes + lnewnodes, key = lambda node: node.heuristic)
        elif self.strategy == 'a*':
            self.open_nodes = sorted(self.open_nodes + lnewnodes, key = lambda node: node.cost + node.heuristic)
