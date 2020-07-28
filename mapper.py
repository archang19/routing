#!/usr/bin/env python3

class Segment:
    def __init__(self, startCoord, endCoord, name):
        """
        :type startCoord: tuple
        :type endCoord: tuple
        :type name: string
        """
        self.start = startCoord
        self.end = endCoord
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
        sound : str
            the sound that the animal makes
        num_legs : int
            the number of legs the animal has (default 4)

        Methods
        -------
        says(sound=None)
            Prints the animals name and what sound it makes
        """

        self.startToSegment = {}
        self.endToSegment = {}

        self.file_path = file_path
        self.load(self.file_path)

    def load(self, file_path):
        """
        :param file_path: path to map data
        :type string
        :returns: nothing
        """
        try:
            with open(file_path) as f:
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
        """
        :param coord: start coordinate
        :type coord: tuple
        :returns: all street segments that start with coordinate
        :rtype: set
        """
        res = set()
        if coord in self.startToSegment.keys():
            res = res.union(self.startToSegment[coord])
        if coord in self.endToSegment.keys():
            res = res.union(self.endToSegment[coord])
        return res





