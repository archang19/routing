#!/usr/bin/env python3

from queue import PriorityQueue
import geometry

class Route:
    def __init__(self, route, dist_traveled):
        """
        A trivial class for use in Router
        ...
        Attributes
        ----------
        :type route: list
           list of street segments
        :type dist_traveled: float
           combined distance of street segments
        """
        self.route = route
        self.dist_traveled = dist_traveled

class Router:
    def __init__(self, mapper):
        """
        A class to find shortest path between two coordinates
        ...
        Attributes
        ----------
        :type mapper: Mapper
            object containing relevant map information
        """
        self.mapper = mapper

    def find_route(self, start, end):
        """
        :param start: tuple for start coordinate
        :param end: tuple for end coordinate
        :return: Route object containing segments in route and distance travelled
        """
        q = PriorityQueue()
        q.put(start, 0)

        cost_so_far = {}

        came_from = {start: None}
        cost_so_far[start] = 0

        route = []
        dist_traveled = 0

        solution = Route(None, None)

        while not q.empty():
            current = q.get()
            if current == end:
                backtrack = end
                while backtrack != start and not(came_from[backtrack] is None):
                    prev = came_from[backtrack]
                    segs = self.mapper.get_segments(prev)
                    for seg in segs:
                        if seg.end == backtrack:
                            route.append(seg)
                            dist_traveled += geometry.dist_mi(seg.start, seg.end)
                            backtrack = prev
                            break
                route.reverse()
                solution = Route(route, dist_traveled)
                return solution

            children = self.mapper.get_segments(current)
            for next in children:
                next_coord = next.end
                new_cost = cost_so_far[current] + geometry.dist_mi(current, next_coord)
                if next_coord not in cost_so_far or new_cost < cost_so_far[next_coord]:
                    cost_so_far[next_coord] = new_cost
                    priority = new_cost + self.heuristic(next_coord, next_coord)
                    q.put(next_coord, priority)
                    came_from[next_coord] = current

        return solution

    def heuristic(self, start, end):
        """
        :param start: tuple of start coordinate
        :param end: tuple of end coordinate
        :return: distance in miles in direct line from start to end

        This is the most appropriate heuristic for this purpose, since the direction
        of movement is not restricted to a finite number of directories (e.g
        north, south, east, west). Other heuristics used for A* include Manhattan
        Distance, which is calculated as abs(x1-x2) + abs(y1-y2).
        """
        return geometry.dist_mi(start, end)

