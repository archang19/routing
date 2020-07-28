#!/usr/bin/env python3

class Segment:
    def __init__(self, start, end, name):
        """
        A class used to represent a street segment
        ...
        Attributes
        ----------
        :type start: tuple
            start coordinate
        :type end: tuple
            end coordinate
        :type name: string
            name of street
        """
        self.start = start
        self.end = end
        self.name = name.rstrip()

class Mapper:
    def __init__(self, file_path):
        """
        A class used to efficiently retrieve map data
        ...
        Attributes
        ----------
        startToSegment : dict
            maps start coordinate to set of street segments
        endToSegment : dict
            maps end coordinate to set of street segments
        file_path : str
            path to map data

        Methods
        -------
        load(self)
            loads data into coordinate to segment dictionaries
        get_segments(self, coord)
            returns set of all segments that begin with coord
        """

        self.startToSegment = {}
        self.endToSegment = {}

        self.file_path = file_path
        self.load()

    def load(self):
        try:
            with open(self.file_path) as f:
                raw_data = f.readlines()
        except:
            return False

        i = 0
        while i < len(raw_data):
            street_name = raw_data[i]
            num_segments = int(raw_data[i+1])
            for j in range(i+2, i+2+num_segments):
                coords = raw_data[j].split()
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





