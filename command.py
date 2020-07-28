#!/usr/bin/env python3


class DeliveryCommand:
    def __init__(self):
        self.type = ""
        self.streetName = None
        self.direction = None
        self.distance = None
        self.item = None

    def init_as_proceed_command (self, dir, streetName, dist):
        self.type = "PROCEED"
        self.streetName = streetName
        self.direction = dir
        self.distance = dist

    def init_as_turn_command(self, dir, streetName):
        self.type = "TURN"
        self.streetName = streetName
        self.direction = dir
        self.distance = 0

    def init_as_deliver_command(self, item):
        self.type = "DELIVER"
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