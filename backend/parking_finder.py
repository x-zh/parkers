# coding=UTF-8
import django
import os
import re
import math

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "parkers.settings")
django.setup()

from dateutil.parser import parse

from backend.models import LocationWithLatLng, Sign

delta_T = 0.007  # 0.0065 is about 0.7 miles.
car_length = 20  # a car needs about 20 feet to park.


def finder(point, dt=None):
    lat = point[0]
    lng = point[1]

    # first layer, filter the location
    kwargs = {
        'lat_main_from__gte': lat - delta_T,
        'lat_main_from__lte': lat + delta_T,
        'lng_main_from__gte': lng - delta_T,
        'lng_main_from__lte': lng + delta_T
    }
    locations = LocationWithLatLng.objects.filter(**kwargs)

    res = []
    for location in locations:
        signs = Sign.objects.filter(code=location.code, status=location.status)
        sanitation_schedule, slots_num = get_sanitation_schedule(signs)
        if not sanitation_schedule:
            continue
        # second layer, filter by date
        if dt and dt.weekday() not in sanitation_schedule['days']:
            continue

        try:
            data = {
                'location': location.main_street,
                'from': (
                    location.from_street,
                    str(location.lat_main_from),
                    str(location.lng_main_from)
                ),
                'to': (
                    location.to_street,
                    str(location.lat_main_to),
                    str(location.lng_main_to)
                ),
                'side': location.side,
                'datetime': {
                    'days': sanitation_schedule['days'],
                    'hours': [str(i.time())[:-3] for i in sanitation_schedule['hours']]
                },
                'cleaned': dt.hour - sanitation_schedule['hours'][1].hour,
                'estimated': slots_num
            }
            if data['cleaned'] <= 2 and data['cleaned'] >= -1:
                res.append(data)
        except:
            print 'chu cuo la !!!'
            pass
        # print location.code, location.status, ',
        # Main: ', location.main_street, get_code(location.code)

    # res.sort(
    #     key=lambda x: x['cleaned'] if x['cleaned'] >= 0 else - x['cleaned'] * 2)
    return res


def get_sanitation_schedule(signs):
    """Get sanitation schedule.
    :param signs: a list of sign
    :return: (schedule, slots_num)
        schedule: (start time, end time, days in week)
        slots_num: estimated number of cars can be parking in the street.
    """
    ssp = SanitationSignParser()
    start_sign, end_sign = None, None
    sanitation_schedule = None
    for (index, sign) in enumerate(signs):
        if 'SANITATION BROOM SYMBOL' in sign.description and not start_sign:
            # If current sign is not the first sign, then get the previous one
            # as the start_sign for calculating the distance.
            if index > 0:
                start_sign = signs[index - 1]
            else:
                start_sign = sign
        if 'SANITATION BROOM SYMBOL' in sign.description:
            # If current sign is not the last sign, then get the next one as
            # the end_sign for calculating the distance.
            if index < len(signs) - 1:
                end_sign = signs[index + 1]
            else:
                end_sign = sign
            # Parse sanitation schedule
            if not sanitation_schedule:
                sanitation_schedule = ssp.parse(sign.description)
    distance = 0
    if start_sign and end_sign:
        distance = abs(end_sign.distance - start_sign.distance)
    return sanitation_schedule, estimate_slots(distance)


class SanitationSignParser():

    '''
    parse sanitation sign into days, hour range
    '''
    WEEKDAY = ['MON', 'TUES', 'WED', 'THURS', 'FRI', 'SAT', 'SUN']
    ABBR = {
        'MONDAY': 'MON', 'TUESDAY': 'TUES', 'WEDNESDAY': 'WED',
        'THURSDAY': 'THURS', 'FRIDAY': 'FRI', 'SATURDAY': 'SAT',
        'SUNDAY': 'SUN'
    }
    DAYS = set(WEEKDAY)

    def process_days(self, daystr):
        '''
        return the weekdays according the daystr
        '''
        for k, v in self.ABBR.items():
            daystr = daystr.replace(k, v)

        res = set()
        if '&' in daystr:
            res = set([i.strip() for i in daystr.split('&')])
        elif 'EXCEPT' in daystr:
            try:
                res = self.DAYS - set(
                    [i.strip() for i in daystr.split(' ')[1].split('&')])
            except IndexError:
                return []
        else:
            res = set([i.strip() for i in daystr.split(' ')])
        return [i for i in range(7) if self.WEEKDAY[i] in res]

    def process_hours(self, hour1, hour2):
        return (parse(hour1), parse(hour2))

    def parse(self, text):
        '''
        return start_time, end_time and days in a week
        '''
        res = {}
        hour = r'(\d{1,2}:?\d{0,2}(AM|PM)?)'
        split = r'(-|( TO ))'
        day = r'\s([\w\ \&]*\w+)\ '
        m = re.findall(hour + split + hour + day, text)
        if m:
            res["hours"] = self.process_hours(m[0][0], m[0][4])
            res["days"] = self.process_days(m[0][6])
        else:
            day = r'(MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY)'
            day = r'((' + day + ' *)+)'
            m = re.findall(day + hour + split + hour, text)
            if m:
                res["hours"] = self.process_hours(m[0][3], m[0][7])
                res["days"] = self.process_days(m[0][0])
        return res


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

(lat - T, lng - T)                              (lat + T, lng - T)
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
(lat - T, lng + T)                              (lat T + T, lng + T)

The intersection points we need to get from database are:

points (x, y) where x >= lat - T && x <= lat + T
                    y >= lng - T && y <= lng + T

Use the intersection points to find all the streets/avenues
that connect with it.

Note:
1. For a street, if one side has fire hydrants, then the other side doesn't.
2. Valid parking place start and end with 'Building Line' or 'Property Line'.
3. Fire hydrant takes two parking spaces.
4. Personal driveway takes one parking space.


Special cases:
,NO PARKING (SANITATION BROOM SYMBOL) 8-11AM MON & THURS SEE R7-84R
9-10:30AM TUES & F RI W

"""
if __name__ == '__main__':
    my_location = (40.6140727, -73.989483)
    finder(my_location)
