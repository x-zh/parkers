# coding=UTF-8

"""
Created on 11/15/14

@author: 'johnqiao'
"""
from django.shortcuts import render_to_response


def google_map(request):
    if request.method == 'GET':
        template_values = {}
        return render_to_response("google_map.html", template_values)