#!/usr/bin/env python3

import router
import geometry
import mapper

class Delivery:
    def __init__(self, item, loc):
        self.item = item
        self.loc = loc

class DeliveryPlanner:
    def __init__(self, path_to_map_file, path_to_deliveries_file):
        self.mapper = mapper.Mapper(path_to_map_file)
        self.router = router.Router(self.mapper)
        self.deliveries = []
        self.commands = []
        self.route = None
        self.prevStreet = None
        self.totalDistanceTravelled = 0
        self.lastProceedIndex = -1
        self.justDelivered = False

        with open(path_to_deliveries_file) as f:
            self.raw_data = f.readlines()
            i = 0
            while i < len(self.raw_data):
                if i == 0:
                    initial_coords = self.raw_data[i].split()
                    self.depot = (float(initial_coords[0]), float(initial_coords[1]))
                else:
                    l = self.raw_data[i].split(":")
                    coords = l[0].split()
                    item = l[1].split("(")[0]
                    d = Delivery(item, (float(coords[0]), float(coords[1])))
                    self.deliveries.append(d)
                i += 1

    def generate_delivery_plan(self):
        cur = self.depot
        last_place = None
        self.just_delivered = False
        self.prevStreet = None

        dCommand = DeliveryCommand()
        self.lastProceedIndex = -1

        for i in range(len(self.deliveries)):
            next = self.deliveries[i].loc
            if i == len(self.deliveries) - 1:
                last_place = next

            self.route = self.router.find_route(cur, next)
            if self.route.route is None or self.route.dist_traveled is None:
                return 0

            self.just_delivered = True
            self.plan_route()

            dCommand.init_as_deliver_command(self.deliveries[i].item)
            self.commands.append(dCommand)
            cur = next

        self.route = self.router.find_route(last_place, self.depot)
        self.just_delivered = True
        self.plan_route()

        return 1

    def plan_route(self):
        streets = self.route.route
        for curStreet in streets:
            angleTurn = 0
            if curStreet != streets[0]:
                angleTurn = geometry.angleBetween2Lines(self.prevStreet, curStreet)
            self.prevStreet = curStreet
            angle = geometry.angleOfLine(curStreet)
            direction = self.set_direction(angle)
            dist = geometry.dist_mi(curStreet.start, curStreet.end)
            self.totalDistanceTravelled += dist

            if self.lastProceedIndex != -1 and curStreet.name == self.commands[self.lastProceedIndex].streetName and (not self.justDelivered):
                self.commands[self.lastProceedIndex].increaseDistance(dist)
                continue
            dCommand = DeliveryCommand()
            if angleTurn < 1 or angleTurn > 359:
                dCommand.init_as_proceed_command(direction, curStreet.name, dist)
            elif angleTurn >= 1 and angleTurn < 180:
                turn_command = DeliveryCommand()
                turn_command.init_as_turn_command("LEFT", curStreet.name)
                if curStreet != streets[0] and not self.justDelivered:
                    self.commands.append(turn_command)
                dCommand.init_as_proceed_command(direction, curStreet.name, dist)
            else:
                turn_command = DeliveryCommand()
                turn_command.init_as_turn_command("RIGHT", curStreet.name)
                if curStreet != streets[0] and not self.justDelivered:
                    self.commands.append(turn_command)
                dCommand.init_as_proceed_command(direction, curStreet.name, dist)

            self.commands.append(dCommand)
            self.lastProceedIndex = len(self.commands) - 1
            self.justDelivered = False

    def set_direction(self, angle):
        if angle >= 0 and angle < 22.5:
            return "EAST"
        elif angle >= 22.5 and angle < 67.5:
            return "NORTHEAST"
        elif angle >= 67.5 and angle < 112.5:
            return "NORTH"
        elif angle >= 112.5 and angle < 157.5:
            return "NORTHWEST"
        elif angle >= 157.5 and angle < 202.5:
            return "WEST"
        elif angle >= 202.5 and angle < 247.5:
            return "SOUTHWEST"
        elif angle >= 247.5 and angle < 292.5:
            return "SOUTH"
        elif angle >= 292.5 and angle < 337.5:
            return "SOUTHEAST"
        else:
            return "EAST"


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

dm = DeliveryPlanner('mapdata.txt','deliveries.txt')
dm.generate_delivery_plan()
for com in dm.commands:
    print(com.description())
print(dm.totalDistanceTravelled)



