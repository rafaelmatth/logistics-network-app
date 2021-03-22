from django.shortcuts import render

from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import JsonResponse, request
from .models import Map

import json
import operator

import datetime

class CreateMap(APIView):
    def post(self, request):
        '''Post method to create a new map, always required the name'''
        req_post = json.loads(request.body)
        name_map = str(req_post['name'])

        new_map = Map.objects.create(name=name_map)
        new_map.save()

        response_data = {
            'id': new_map.id,
            'map_name': new_map.name,
        }

        return JsonResponse({'message': 'success when registering a map', 'data': response_data}, safe=False)