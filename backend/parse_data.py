# coding=UTF-8

"""
Created on 9/5/14

@author: 'johnqiao'

request URL:
    https://maps.googleapis.com/maps/api/js/GeocodeService.Search?4sEAST%20TREMONT%20AVENUE%20and%20ARTHUR%20AVENUE%2C%20Bronx&7sUS&9sen&callback=_xdc_._jz4d5&token=57297

"""
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Parkers.settings")

import csv
import json
import urllib2
import sys
from backend.models import LocationWithLatLng


def process(file_path):
    count = 0
    test_count = 1
    with open(file_path, 'rb') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            count += 1
            # 0 - Borough code (B - Bronx, K – Brooklyn, M – Manhattan, Q – Queens, Staten Island)
            # 1 - ‘Status’ - order number
            # 2 - Main Street
            # 3 - From Street
            # 4 - To Street
            # 5 - Side of street (N - north, S - south, E - east, W - west)
            code = row[0].strip()
            status = row[1].strip()
            main_street = row[2].strip()
            from_street = row[3].strip()
            to_street = row[4].strip()
            side = row[5].strip()

            area = GetCode(code)

            location_from_street = main_street + ' and ' + from_street + ', ' + area
            location_info_from = fetchLatLng(location_from_street)

            location_to_street = main_street + ' and ' + to_street + ', ' + area
            location_info_to = fetchLatLng(location_to_street)

            location = LocationWithLatLng()
            location.code = code
            location.status = status
            location.main_street = main_street
            location.from_street = from_street
            location.to_street = to_street
            location.side = side
            location.lat_main_from = location_info_from['lat']
            location.lng_main_from = location_info_from['lng']
            location.lat_main_to = location_info_to['lat']
            location.lng_main_to = location_info_to['lng']
            location.save()

            if count == test_count:
                # break
                pass


def fetchLatLng(address):
    user_agent = ('Mozilla/5.0 (Windows NT 6.1; rv:9.0) '
                  + 'Gecko/20100101 Firefox/9.0')
    headers = {'User-Agent': user_agent}
    url = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=true' % address
    url = url.replace(' ', '%20')
    request = urllib2.Request(url=url, headers=headers)
    try:
        data = urllib2.urlopen(request).read()
        json_data = json.loads(data)
        location_info = json_data['results'][0]['geometry']['location']
        print 'address: ', address
        print 'lat: ', location_info['lat'], 'lng: ', location_info['lng']
        return location_info
    except:
        print sys.exc_info()


def GetCode(v):
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
    process('../data/locations.csv')

