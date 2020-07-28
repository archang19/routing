#!/usr/bin/env python3

import math

def deg2rad(deg):
    return deg * math.pi / 180

def rad2deg(rad):
    return rad * 180 / math.pi


def dist_km(coord1, coord2):
    earthRadiusKm = 6371.0
    lat1r = deg2rad(coord1[0])
    lon1r = deg2rad(coord1[1])
    lat2r = deg2rad(coord2[0])
    lon2r = deg2rad(coord2[1])
    u = math.sin((lat2r - lat1r) / 2)
    v = math.sin((lon2r - lon1r) / 2)
    return 2 * earthRadiusKm * math.asin(math.sqrt(u * u + math.cos(lat1r) * math.cos(lat2r) * v * v))

def dist_mi(coord1, coord2):
    milesPerKm = 1 / 1.609344
    return dist_km(coord1, coord2) * milesPerKm



def angleOfLine(line):
    angle = math.atan2(line.end[0] - line.start[0], line.end[1] - line.start[1])
    result = rad2deg(angle)
    if result < 0:
        result += 360
    return result


def angleBetween2Lines(line1, line2):
    angle1 = math.atan2(line1.end[0] - line1.start[0], line1.end[1] - line1.start[1])
    angle2 = math.atan2(line2.end[0] - line2.start[0], line2.end[1] - line2.start[1])
    result = rad2deg(angle2 - angle1)
    if result < 0:
        result += 360
    return result
