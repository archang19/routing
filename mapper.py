#!/usr/bin/env python3

import router

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


m = Mapper('mapdata.txt')

s = (34.0547000, -118.4794734)
e = (34.0857385, -118.4956111)
r = router.Router(m)
a1 = r.find_route(s, e)

print(a1.dist_traveled)
print(len(a1.route))



