#!/usr/bin/env python3

from queue import PriorityQueue
import conversions

class Segment:
    def __init__(self, startCoord, endCoord, name):
        self.start = startCoord
        self.end = endCoord
        self.name = name

class Mapper:
    def __init__(self, file_path):
        # maps coordinate to set of segments
        self.startToSegment = {}
        self.endToSegment = {}

        self.raw_data = None
        self.file_path = file_path
        self.load(self.file_path)

    def load(self, file_path):
        try:
            with open(file_path) as f:
                self.raw_data = f.readlines()
        except:
            return False

        i = 0
        while i < len(self.raw_data):
            street_name = self.raw_data[i]
            num_segments = int(self.raw_data[i+1])
            for j in range(i+2, i+2+num_segments):
                coords = self.raw_data[j].split()
                coord1 = (float(coords[0]), float(coords[1]))
                coord2 = (float(coords[2]), float(coords[3]))
                seg1 = Segment(coord1, coord2, street_name)
                seg2 = Segment(coord2, coord1, street_name)

                if coord1 not in self.startToSegment.keys():
                    self.startToSegment[coord1] = set()
                self.startToSegment[coord1].add(seg1)

                if coord2 not in self.endToSegment.keys():
                    self.endToSegment[coord2] = set()
                self.endToSegment[coord2].add(seg2)
            i = j+1

    def get_segments(self, coord):
        res = set()
        if coord in self.startToSegment.keys():
            res = res.union(self.startToSegment[coord])
        if coord in self.endToSegment.keys():
            res = res.union(self.endToSegment[coord])
        return res

class Route:
    def __init__(self, route, dist_traveled):
        self.route = route
        self.dist_traveled = dist_traveled


class Router:
    def __init__(self, mapper):
        self.mapper = mapper

    def find_route(self, start, end):
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
                while backtrack != start:
                    prev = came_from[backtrack]
                    segs = m.get_segments(prev)
                    for seg in segs:
                        if seg.end == backtrack:
                            route.append(seg)
                            dist_traveled += conversions.dist_mi(seg.start, seg.end)
                            backtrack = prev
                            break
                solution = Route(route, dist_traveled)

            children = self.mapper.get_segments(current)
            for next in children:
                next_coord = next.end
                new_cost = cost_so_far[current] + conversions.dist_mi(current, next_coord)
                if next_coord not in cost_so_far or new_cost < cost_so_far[next_coord]:
                    cost_so_far[next_coord] = new_cost
                    priority = new_cost + self.heuristic(next_coord, next_coord)
                    q.put(next_coord, priority)
                    came_from[next_coord] = current

        return solution

    def heuristic(self, start, end):
        dx = abs(start[0] - end[0])
        dy = abs(start[1] - end[1])
        return dx + dy


m = Mapper('mapdata.txt')

s = (34.0547000, -118.4794734)
e = (34.0857385, -118.4956111)
r = Router(m)
a1 = r.find_route(s, e)

print(a1.dist_traveled)
print(len(a1.route))



