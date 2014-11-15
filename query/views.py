import json
from django.shortcuts import render
from django.http import HttpResponse
from backend.parking_finder import finder


def main(request):
    if request.method == 'GET':
        return render(request, 'query.html')
    location = (float(request.POST.get('latitude')),
                float(request.POST.get('longtitude')))
    query_result = finder(location)
    return HttpResponse(json.dumps(query_result),
                        content_type='application/json')

