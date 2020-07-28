#!/usr/bin/env python3

class DeliveryCommand:
    def __init__(self, type, direction=None, streetName=None, distance=None, item=None):
        """
        :param type: string (TURN, PROCEED, or DELIVER)
        :param direction: string (e.g. NORTH, NORTHEAST, EAST, etc.)
        :param streetName: string (e.g. 10th Helena Drive)
        :param distance: float
        :param item: string (i.e. Salad)

        A trivial class for handling the final outputted delivery instructions.
        """
        self.type = type
        self.streetName =streetName
        self.direction = direction
        self.distance = distance
        self.item = item

    def increaseDistance (self, amt):
        self.distance += amt

    def description(self):
        if self.type == "TURN":
            return "TURN " + self.direction + " ON " + self.streetName
        elif self.type == "PROCEED":
            return "PROCEED " + self.direction + " ON " + self.streetName + " FOR " + "{:.2f}".format(self.distance) + " MILES"
        elif self.type == "DELIVER":
            return "DELIVER " + self.item