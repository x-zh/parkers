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

from backend.models import LocationWithLatLng, Sign

delta_T = 0.0010  # 0.0065 is about 0.7 miles


def finder(point):
    lat = point[0]
    lng = point[1]

    locations = LocationWithLatLng.objects.filter(lat_main_from__gte=lat-delta_T,
                                                  lat_main_from__lte=lat+delta_T,
                                                  lng_main_from__gte=lng-delta_T,
                                                  lng_main_from__lte=lng+delta_T)
    for location in locations:
        print '------------------------------------'
        print location.code, location.status, ', Main: ', location.main_street, get_code(location.code)
        print 'From: %s (%f, %f), To: %s (%f, %f)' % (location.from_street, float(location.lat_main_from), float(location.lng_main_from),
                                                      location.to_street, float(location.lat_main_to), float(location.lng_main_to))
        # Get the sign info
        signs = Sign.objects.filter(code=location.code, status=location.status)
        for sign in signs:
            print sign.sequence, '%5s' % sign.distance, '%5s' % sign.arrow, sign.description
        print ''


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

