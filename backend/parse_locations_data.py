# coding=UTF-8

"""
Created on 9/5/14

@author: 'johnqiao'

Convert address data to latitude and longitude data.

Geocoding API

request URL:
    https://maps.googleapis.com/maps/api/js/GeocodeService.Search?4sEAST%20TREMONT%20AVENUE%20and%20ARTHUR%20AVENUE%2C%20Bronx&7sUS&9sen&callback=_xdc_._jz4d5&token=57297

Day limit 1250 requests, should use different IPs.

DATA SIZE: 94107 (updated 10/31/2014 by John Qiao)

"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Parkers.settings")

import csv
import json
import time
import urllib2
import sys
import hashlib
import hmac
import base64
import urlparse
from backend.models import LocationWithLatLng, Location

KEY = '21499889482-0hdh8qgo45cr38sui06damoqp5co4j5l.apps.googleusercontent.com'


def process_file(file_path):
    count = 0
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

            area = get_code(code)

            # Check if this data has already been fetched.
            if LocationWithLatLng.objects.filter(code=code, status=status).exists():
                continue

            location_from_street = main_street + ' and ' + from_street + ', ' + area
            location_info_from = fetch_lat_lng(location_from_street)

            location_to_street = main_street + ' and ' + to_street + ', ' + area
            location_info_to = fetch_lat_lng(location_to_street)

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

            time.sleep(0.30)

            print 'count: ', count


def process_db(start_index):
    count = start_index

    rows = process_db_yield(start_index)
    while True:
        try:
            row = rows.next()
            count += 1
            # 0 - Borough code (B - Bronx, K – Brooklyn, M – Manhattan, Q – Queens, Staten Island)
            # 1 - ‘Status’ - order number
            # 2 - Main Street
            # 3 - From Street
            # 4 - To Street
            # 5 - Side of street (N - north, S - south, E - east, W - west)
            code = row.code.strip()
            status = row.status.strip()
            main_street = row.main_street.strip()
            from_street = row.from_street.strip()
            to_street = row.to_street.strip()
            side = row.side.strip()

            area = get_code(code)

            # Check if this data has already been fetched.
            if LocationWithLatLng.objects.filter(code=code, status=status).exists():
                continue

            location_from_street = main_street + ' and ' + from_street + ', ' + area
            location_info_from = fetch_lat_lng(location_from_street)

            location_to_street = main_street + ' and ' + to_street + ', ' + area
            location_info_to = fetch_lat_lng(location_to_street)

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

            time.sleep(0.30)
            print 'count: ', count
        except StopIteration:
            break
        except:
            error = "Unexpected error:", sys.exc_info()
            break


def process_db_yield(start_index):
    rows = Location.objects.filter(id__gte=start_index)
    for row in rows:
        yield row


def fetch_lat_lng(address):
    user_agent = ('Mozilla/5.0 (Windows NT 6.1; rv:9.0) '
                  + 'Gecko/20100101 Firefox/9.0')
    headers = {'User-Agent': user_agent}
    # url = 'http://maps.googleapis.com/maps/api/geocode/json?client=%s&address=%s&sensor=true' % (KEY, address)
    url = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=true' % address
    url = url.replace(' ', '%20')
    # url = sign_url(url)
    print url
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


def sign_url(url):
    # Convert the URL string to a URL, which we can parse
    # using the urlparse() function into path and query
    # Note that this URL should already be URL-encoded
    url = urlparse.urlparse(url)

    privateKey = "-----BEGIN PRIVATE KEY-----\nMIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBAL1Oc55+pbGuJWxT\no9xeGuQ14Pz/R0+ax/DSfQNQ2VQHKul3EA8O/Pr5qmOFaDU5hE3Up8lBI6tKeR84\nbSwCM5O/BEYvzijKYgEtaSRmaGpE506y6b+12nf5H9Mb8FD5R+YIL5ZYfY7Yzewb\ngyhZFOEnzfO80ky2JTwb9ser9uadAgMBAAECgYBT1kqeBria1+T69I+9KHAAYVwi\nr2uFdabWoGF89nFJJWN7wZ77DEg9XhR3vr1H1REi5urn1lFVqsW5bePreY4dPX+p\nUsZo3r5EDvqh0nf3IK3l3WR9Cp7bXg9ab9o0rUF4S1CAu66iQkU20KzFWIxeO48i\nFQ8EZVnqkPJh8/KigQJBAOP3N8i6PLt1kEDoAITtOJHfYiuQ3x5oP3ZPtREsR1kU\nPSTPUKCKJzctJiatofhUrpjKp+iSTA51/JFjrSIiuN8CQQDUlitPy2wnapTvVqeT\nWl5cDcsfq6AbAq30LrysT/5FH0nwkG5BRUZ1h/8PVXjIdlRbztGUB1QFZ/skJSRc\nfMQDAkEAx1d6tFAGo3XeOqOlMJevi/9mfOol8RT/yZlRoD6z9TU5cmLHAltMh3c3\nkULsC5chRgKQaVLkpxCNVyVuVBdAyQJBAI5bGRnQENa8SouTLZhBFZrzKahFl2s+\n+hngCjwhPRYwg6TyMsLGjw45SZWNGNq0Un1AG5vS5HLSVJy5uoWsjt0CQQCTYSMS\nokKlssrYAg4bxCcxqfpfkgmIIg+5WF5WASY+/9ddI4sRKTDzrrbbVe7M7bwXDYSK\nXzWO+qiZh7CwLXxF\n-----END PRIVATE KEY-----\n"

    # We only need to sign the path+query part of the string
    urlToSign = url.path + "?" + url.query

    # Decode the private key into its binary format
    decodedKey = base64.urlsafe_b64decode(privateKey)

    # Create a signature using the private key and the URL-encoded
    # string using HMAC SHA1. This signature will be binary.
    signature = hmac.new(decodedKey, urlToSign, hashlib.sha1)

    # Encode the binary signature into base64 for use within a URL
    encodedSignature = base64.urlsafe_b64encode(signature.digest())
    originalUrl = url.scheme + "://" + url.netloc + url.path + "?" + url.query

    fullUrl = originalUrl + "&signature=" + encodedSignature

    return fullUrl


if __name__ == '__main__':
    # process_file('../data/locations.csv')
    count = LocationWithLatLng.objects.all().count()
    process_db(count - 10)