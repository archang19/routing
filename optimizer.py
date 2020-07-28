#!/usr/bin/env python3

import geometry
from sys import maxsize
from itertools import permutations

class Optimizer:
    def __init__(self, deliveries, source):
        """
        :param deliveries: list of Delivery objects
        :param source: tuple for source (depot) coordinates

        A class for optimizing delivery order. Implements solution to
        Travelling Salesman Problem.
        """
        self.deliveries = deliveries
        self.source = source

    def simple_TSP(self):
        """
        :return: re-ordered delivery list

        Naive solution to Travelling Salesman Problem. Generates all possible
        permutations of ordering. Uses Euclidean distance to approximate true
        distance, as exact computation would be too expensive.

        Complexity is O(n!), so not feasible for large n.
        """

        min_path = maxsize
        min_perm = 0

        perms = list(permutations(range(0, len(self.deliveries))))
        for i in range(0, len(perms)):
            perm = perms[i]
            cur_cost = 0
            cur_loc = self.source
            for j in perm:
                cur_cost += geometry.dist_mi(cur_loc, self.deliveries[j].loc)
                cur_loc = self.deliveries[j].loc
            cur_cost += geometry.dist_mi(cur_loc, self.source)
            if cur_cost < min_path:
                min_perm = i
                min_path = cur_cost

        return [self.deliveries[i] for i in perms[min_perm]]

    def greedy_TSP(self):
        """
        :return: re-ordered delivery list

        Simple (non-optimal) algorithm. Choose the next closest delivery location
        until all delivery locations have been visited
        """
        cur_loc = self.source
        visited = set()
        sol = []
        while len(visited) < len(self.deliveries):
            min_cost = maxsize
            min_deliv = None
            for delivery in self.deliveries:
                if delivery not in visited:
                    additional_cost = geometry.dist_mi(cur_loc, delivery.loc)
                    if additional_cost < min_cost:
                        min_cost = additional_cost
                        min_deliv = delivery
            visited.add(min_deliv)
            sol.append(min_deliv)
        return sol

