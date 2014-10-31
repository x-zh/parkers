# coding=UTF-8

"""
Created on 9/9/14

@author: 'johnqiao'

The following code returns the distance between to locations based on each point's longitude and latitude.
The distance returned is relative to Earth's radius.

To get the distance in miles, multiply by 3959.
To get the distance in kilometers, multiply by 6373.

"""

import math


def distance(origin, destination, radius):
    lat1, lon1 = origin
    lat2, lon2 = destination

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
                                                  * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


def get_distance_in_m(origin, destination):
    return distance(origin, destination, 3959)


def get_distance_in_km(origin, destination):
    return distance(origin, destination, 6373)


if __name__ == '__main__':
    origin = (40.6162531, -73.986802)
    destination = (40.6091263, -73.9935581)

    print origin[0] - destination[0]
    print origin[1] - destination[1]

    print get_distance_in_m(origin, destination), 'miles'
    print get_distance_in_km(origin, destination), 'kilometers'
