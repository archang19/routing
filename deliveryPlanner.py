#!/usr/bin/env python3

import router
import geometry
import mapper
import delivery
import command
import optimizer

class DeliveryPlanner:
    def __init__(self, path_to_map_file, path_to_deliveries_file):
        """
        A class used to create final delivery routing instructions
        ...
        Attributes
        ----------
        :type mapper: Mapper
            object containing all relevant geocoordinate/segment information
        :type router: Router
            object for calculating optimal route between 2 coordinates
        :type deliveries: Delivery
            list of deliveries to be made
        :type commands: DeliveryCommand
            list of delivery commands (e.g. proceed, turn, deliver)
        :type route: Route
            stores current route that is being converted to delivery instructions
        :type prevStreet: Segment
            stores previous street segment, for use in calculating angles for turns
        :type totalDistanceTravelled: float
            stores total distance traveled (includes all deliveries and return trip)
        :type lastProceedIndex: int
            stores index of last proceed commmand in command list
        :type justDelivered: bool
            stores whether a delivery was just made
        :type depot: tuple
            start coordinates of depot
        :type optimizer: Optimizer
            object for finding optimal delivery order
        """
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
            raw_data = f.readlines()
            i = 0
            while i < len(raw_data):
                if i == 0:
                    initial_coords = raw_data[i].split()
                    self.depot = (float(initial_coords[0]), float(initial_coords[1]))
                else:
                    l = raw_data[i].split(":")
                    coords = l[0].split()
                    item = l[1].split("(")[0]
                    d = delivery.Delivery(item, (float(coords[0]), float(coords[1])))
                    self.deliveries.append(d)
                i += 1

        self.optimizer = optimizer.Optimizer(self.deliveries, self.depot)
        self.deliveries = self.optimizer.simple_TSP()

    def generate_delivery_plan(self):
        cur = self.depot
        last_place = None

        for i in range(len(self.deliveries)):
            next = self.deliveries[i].loc
            if i == len(self.deliveries) - 1:
                last_place = next

            self.route = self.router.find_route(cur, next)
            if self.route.route is None or self.route.dist_traveled is None:
                return False

            self.just_delivered = True
            self.plan_route()

            dCommand = command.DeliveryCommand("DELIVER",None,None,None,self.deliveries[i].item)
            self.commands.append(dCommand)
            cur = next

        self.route = self.router.find_route(last_place, self.depot)
        self.just_delivered = True
        self.plan_route()

        return True

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

            if angleTurn < 1 or angleTurn > 359:
                pass
            elif angleTurn >= 1 and angleTurn < 180:
                turn_command = command.DeliveryCommand("TURN", "LEFT", curStreet.name, None, None)
                if curStreet != streets[0] and not self.justDelivered:
                    self.commands.append(turn_command)
            else:
                turn_command = command.DeliveryCommand("TURN", "RIGHT", curStreet.name, None, None)
                if curStreet != streets[0] and not self.justDelivered:
                    self.commands.append(turn_command)

            dCommand = command.DeliveryCommand("PROCEED", direction, curStreet.name, dist, None)
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

    def print_directions(self):
        print("STARTING FROM: " + str(self.depot))
        for com in self.commands:
            print(com.description())
        print("TOTAL DISTANCE TRAVELED: " + "{:.2f}".format(self.totalDistanceTravelled) + " MILES")


dm = DeliveryPlanner('mapdata.txt','deliveries.txt')
if dm.generate_delivery_plan():
    dm.print_directions()
else:
    print ("No route found")



