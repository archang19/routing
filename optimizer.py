#!/usr/bin/env python3

import geometry
from sys import maxsize
from itertools import permutations

class Optimizer:
    def __init__(self, deliveries, source):
        self.deliveries = deliveries
        self.source = source

    def simple_TSP(self):
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

