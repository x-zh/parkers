import json

from django.http import HttpResponse
from django.shortcuts import render
from .models import Notify


def post_notify(request):
    n = Notify()
    n.title = request.GET.get('title', '')
    n.lat = request.GET.get('latitude', 0)
    n.lng = request.GET.get('longitude', 0)
    n.save()
    return HttpResponse()


def get_notify(request):
    res = []
    for n in Notify.objects.filter().order_by('-datetime'):
        res.append({
            'title': n.title,
            'latitude': str(n.lat),
            'longitude': str(n.lng),
            'datetime': str(n.datetime)
        })
    return HttpResponse(json.dumps(res),
                        content_type='application/json')
