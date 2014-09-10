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

Note:
1. For a street, if one side has fire hydrants, then the other side doesn't.
2. Valid parking place should start and end with 'Building Line' or 'Property Line'.
3. Fire hydrant takes two parking spaces.
4. Personal driveway takes one parking space.


Special cases:
,NO PARKING (SANITATION BROOM SYMBOL) 8-11AM MON & THURS SEE R7-84R
9-10:30AM TUES & F RI W

'''


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Parkers.settings")

import math
from backend.models import LocationWithLatLng, Sign

delta_T = 0.0010  # 0.0065 is about 0.7 miles.
car_length = 20  # a car needs about 20 feet to park.


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
        print 'From: %s (%f, %f), To: %s (%f, %f), Side: %s' % (location.from_street, float(location.lat_main_from), float(location.lng_main_from),
                                                                location.to_street, float(location.lat_main_to), float(location.lng_main_to),
                                                                location.side)
        # 1. Print the sign info.
        # 2. Find the start point and end point.
        signs = Sign.objects.filter(code=location.code, status=location.status)
        start_sign, end_sign = None, None
        # if start_sign or end_sign is None, which means there is no 'Building Line' or 'Property Line' in sign description,
        # then use start_sign_tmp or end_sign_tmp instead.
        start_sign_tmp, end_sign_tmp = None, None
        for sign in signs:
            haha(sign)
            if ('Building Line' in sign.description or 'Property Line' in sign.description) and not start_sign:
                start_sign = sign
            elif ('Building Line' in sign.description or 'Property Line' in sign.description) and not end_sign:
                end_sign = sign
            if 'Curb Line' in sign.description:
                if not start_sign_tmp:
                    start_sign_tmp = sign
                elif not end_sign_tmp:
                    end_sign_tmp = sign
            # print sign.sequence, '%5s' % sign.distance, '%5s' % sign.arrow, sign.description
        if not start_sign:
            start_sign = start_sign_tmp
        if not end_sign:
            end_sign = end_sign_tmp
        if start_sign and end_sign:
            print 'Estimated parking slots: ', estimate_slots(end_sign.distance - start_sign.distance)
        print ''


def haha(sign):
    """Get sanitation schedule.
    """
    import re
    m = re.findall(r'(\d{1,2}:?\d{0,2}((A|P)M)?)(-|( TO ))(\d{1,2}:?\d{0,2}((A|P)M)?)\s([\w\ \&]*\w+)\ ', sign.description)
    if m:
        m = m[0]
        print m[0], m[5], m[8]


def estimate_slots(length):
    return int(math.floor(length / car_length))


def get_sanitation_schedule(signs):
    """
    :param signs: a list of signs of the street.
    :return:
    """
    start_sign, end_sign = None, None
    for (index, sign) in enumerate(signs):
        if 'SANITATION BROOM SYMBOL' in sign.description and not start_sign:
            start_sign = sign
        if 'SANITATION BROOM SYMBOL' in sign.description:
            end_sign = sign


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

