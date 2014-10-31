# coding=UTF-8

"""
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

"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Parkers.settings")

import math
from backend.models import LocationWithLatLng, Sign

delta_T = 0.0010  # 0.0065 is about 0.7 miles.
car_length = 20  # a car needs about 20 feet to park.


def finder(point):
    lat = point[0]
    lng = point[1]

    locations = LocationWithLatLng.objects.filter(lat_main_from__gte=lat - delta_T,
                                                  lat_main_from__lte=lat + delta_T,
                                                  lng_main_from__gte=lng - delta_T,
                                                  lng_main_from__lte=lng + delta_T)
    for location in locations:
        print '------------------------------------'
        print location.code, location.status, ', Main: ', location.main_street, get_code(location.code)
        print 'From: %s (%f, %f), To: %s (%f, %f), Side: %s' % (location.from_street, float(location.lat_main_from), float(location.lng_main_from),
                                                                location.to_street, float(location.lat_main_to), float(location.lng_main_to),
                                                                location.side)
        signs = Sign.objects.filter(code=location.code, status=location.status)
        # for sign in signs:
        # print sign.sequence, '%5s' % sign.distance, '%5s' % sign.arrow, sign.description

        sanitation_schedule, slots_num = get_sanitation_schedule(signs)
        if sanitation_schedule and slots_num:
            print 'Sanitation schedule: %s-%s, %s' % (sanitation_schedule[0], sanitation_schedule[1], sanitation_schedule[2])
            print 'Estimated parking slots: ', slots_num
        print ''


def get_sanitation_schedule(signs):
    """Get sanitation schedule.
    :param signs: a list of sign
    :return: (schedule, slots_num)
        schedule: (start time, end time, days in week)
        slots_num: estimated number of cars can be parking in the street.
    """

    start_sign, end_sign = None, None
    sanitation_schedule = None
    for (index, sign) in enumerate(signs):
        if 'SANITATION BROOM SYMBOL' in sign.description and not start_sign:
            # If current sign is not the first sign, then get the previous one as the start_sign for calculating the distance.
            if index > 0:
                start_sign = signs[index - 1]
            else:
                start_sign = sign
        if 'SANITATION BROOM SYMBOL' in sign.description:
            # If current sign is not the last sign, then get the next one as the end_sign for calculating the distance.
            if index < len(signs) - 1:
                end_sign = signs[index + 1]
            else:
                end_sign = sign
            # Parse sanitation schedule
            if not sanitation_schedule:
                sanitation_schedule = parse_sanitation_schedule_date(sign.description)
    distance = 0
    if start_sign and end_sign:
        distance = abs(end_sign.distance - start_sign.distance)
    return sanitation_schedule, estimate_slots(distance)


def parse_sanitation_schedule_date(text):
    import re

    m = re.findall(r'(\d{1,2}:?\d{0,2}((A|P)M)?)(-|( TO ))(\d{1,2}:?\d{0,2}((A|P)M)?)\s([\w\ \&]*\w+)\ ', text)
    if m:
        m = m[0]
        return m[0], m[5], m[8]


def estimate_slots(length):
    return int(math.floor(length / car_length))


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
