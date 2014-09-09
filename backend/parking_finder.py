# coding=UTF-8

'''
Created on 9/9/14

@author: 'johnqiao'

----------------------------------------
|  |  |  |  |  |  |  |  |  |  |  |  |  |
----------------------------------------
|  |  |  |  |  |  |  |  |  |  |  |  |  |
----------------------------------------
|  |  |  |  |  |  |  |  |  |  |  |  |  |
----------------------------------------
|  |  |  |  |  |  |  | D|  |  |  |  |  |
----------------------------------------
|  |  |  |  |  |  |  |  |  |  |  |  |  |
----------------------------------------
|  |  |  |  |  |  |  |  |  |  |  |  |  |
----------------------------------------

Destination point D's location is (lat, lng).

Use a delta T to locate a box area which we use it to further find
all the parking places.

Top: (lat - T, lng)
Right: (lat, lng + T)
Bottom: (lat + T, lng)
Left: (lat, lng - T)

The the box area is:

(lat - T, lng - T)                              (lat - T, lng + T)
                --------------------------------
                |                              |
                |                              |
                |                              |
                |                              |
                |               D              |
                |                              |
                |                              |
                |                              |
                |                              |
                --------------------------------
(lat - T, lng + T)                              (lat T T, lng + T)

The intersection points we need to get from database are:

points (x, y) where x >= lat - T && x <= lat + T
                    y >= lng - T && y <= lng + T

Use the intersection points to find all the streets/avenues
that connect with it.

'''

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Parkers.settings")

from backend.models import LocationWithLatLng

delta_T = 0.0015  # 0.0065 about 0.7 miles


def finder(point):
    lat = point[0]
    lng = point[1]

    locations = LocationWithLatLng.objects.filter(lat_main_from__gte=lat-delta_T,
                                                  lat_main_from__lte=lat+delta_T,
                                                  lng_main_from__gte=lng-delta_T,
                                                  lng_main_from__lte=lng+delta_T)

    intersections = []
    for location in locations:
        has_location = False
        for intersection in intersections:
            if (location.main_street == intersection.main_street and location.from_street == intersection.from_street) or \
                    (location.from_street == intersection.main_street and location.main_street == intersection.from_street):
                has_location = True
                break
        if not has_location:
            intersections.append(location)

    print 'Total # of the results: ', len(intersections)
    for intersection in intersections:
        print intersection.main_street, 'and', intersection.from_street + ',', get_code(intersection.code)


def get_code(v):
    if 'B' in v:
        return 'Bronx'
    elif 'K' in v:
        return 'Brooklyn'
    elif 'M':
        return 'Manhattan'
    elif 'Q':
        return 'Queens'
    elif 'S':
        return 'Staten Island'
    print 'Error: Borough code not found!!'


if __name__ == '__main__':
    my_location = (40.878732, -73.8642857)
    finder(my_location)
    pass

