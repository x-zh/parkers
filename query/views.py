import json
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse

from dateutil.parser import parse
from oauth2_provider.decorators import protected_resource
from backend.parking_finder import finder


def finderHelper(request):
    res = []
    if request.method == 'POST':
        req_data = request.POST
        location = (float(req_data.get('latitude')),
                    float(req_data.get('longitude')))
        dt = datetime.now()
        if req_data.get('datetime'):
            dt = parse(req_data.get('datetime'))
        res = finder(location, dt)
    return res


@csrf_exempt
@protected_resource()
def api_call(request):
    res = finderHelper(request)
    return HttpResponse(json.dumps(res),
                        content_type='application/json')


def main(request):
    if request.method == 'GET':
        return render(request, 'query.html')
    res = finderHelper(request)
    return HttpResponse(json.dumps(res),
                        content_type='application/json')
    # return render(request, 'query.html', {'res': res})
