from django.shortcuts import render

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated

from django.http import JsonResponse, request
from .models import Map, LogisticsNetwork, Cities

import json


class CreateMap(APIView):
    def post(self, request):
        '''Post method to create a new map, always required the name'''
        req_post = json.loads(request.body)
        name_map = str(req_post['name'])

        filter_maps = Map.objects.all()

        '''Checking if a map with the requested name already exists'''
        if filter_maps.count() > 0:
            for map_class in filter_maps:
                if map_class.name == name_map:
                    return JsonResponse(status=400, data={'message': 'map name already registered'})
                    break

        '''Saving new map'''
        new_map = Map.objects.create(name=name_map)
        new_map.save()

        response_data = {
            'message': 'success when registering a map',
            'data': {
                'id': new_map.id,
                'map_name': new_map.name,
            }
        }

        return JsonResponse(response_data, safe=False)


class ListLogisticNetwork(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        maps = Map.objects.all()
        logistics_networks = LogisticsNetwork.objects.all()

        response_data = []
        for map_data in maps:
            data = {
                'id': map_data.id,
                'map_name': map_data.name,
                'logistics_network': []
            }

            for logistic_network in logistics_networks:
                logistic_data = {
                    'id': logistic_network.id,
                    'origin_city':  logistic_network.origin_city.name,
                    'destination_city':  logistic_network.destination_city.name,
                    'distance  ':  logistic_network.distance
                }

                data['logistics_network'].append(logistic_data)

            response_data.append(data)

        return JsonResponse(response_data, safe=False)


class CreateLogisticNetwork(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        '''Post method to create a new map, always required the name'''
        req_post = json.loads(request.body)
        try:
            map_name = str(req_post['map_name'])
            origin_city = str(req_post['origin_city'])
            destination_city = str(req_post['destination_city'])
            distance = float(req_post['distance'])
        except:
            return JsonResponse(status=406, data={'message': 'wrong data format'})

        '''Check that the names of the cities of origin and destination are the same'''
        if origin_city == destination_city:
            return JsonResponse(status=406, data={'message': 'name of city of origin and destination cannot be the same'})

        '''Method to create or call an object of the city model'''
        get_origin_city = Cities.objects.get_or_create(name=origin_city)[0]
        get_destination_city = Cities.objects.get_or_create(name=destination_city)[
            0]

        '''Check if the map exists and register a new logistics network'''
        try:
            get_map = Map.objects.get(name=map_name)

            new_logistic_network = LogisticsNetwork.objects.create(
                map_network=get_map, origin_city=get_origin_city, destination_city=get_destination_city, distance=distance)

            new_logistic_network.save()

            response_data = {
                'message': 'success when registering a logistic network',
                'data': {
                    'id': new_logistic_network.id,
                    'origin_city': origin_city,
                    'destination_city': destination_city,
                    'distance': new_logistic_network.distance,
                }
            }

            return JsonResponse(response_data, safe=False)

        except:
            return JsonResponse(status=406, data={'message': 'map name not found'})


class GetTravelValue(APIView):
    def post(self, request):
        req_post = json.loads(request.body)
        try:
            map_name = str(req_post['map_name'])
            origin_city = str(req_post['origin_city'])
            destination_city = req_post['destination_city']
            vehicle_autonomy = float(req_post['vehicle_autonomy'])
            fuel_value = float(req_post['fuel_value'])
        except:
            return JsonResponse(status=406, data={'message': 'wrong data format'})

        citie_origin = Cities.objects.get(name=origin_city)
        citie_destination = Cities.objects.get(name=destination_city)

        def __sum_total_distance(distance_origin, distance_destination):
            return distance_origin + distance_destination

        def __calculate_travel_cost(total_distance, vehicle_autonomy, fuel_value):
            return total_distance / vehicle_autonomy * fuel_value

        try:
            logistic = LogisticsNetwork.objects.filter(
                origin_city=citie_origin, destination_city=citie_destination).order_by('distance')

            travel_cost = __calculate_travel_cost(
                float(logistic[0].distance), vehicle_autonomy, fuel_value)

            data = {
                'route': f'{logistic[0].origin_city.name} {logistic[0].destination_city.name}',
                'cost': travel_cost
            }

            return JsonResponse(data, safe=False)

        except:
            origins = LogisticsNetwork.objects.filter(origin_city=citie_origin)
            destinations = LogisticsNetwork.objects.filter(
                destination_city=citie_destination)

            for origin in origins:
                min_distance_origin = float(origins[0].distance)

                citie_origin_origin = origins[0].origin_city.name

                destination_origin_city = origins[0].destination_city.name

                if float(origin.distance) < min_distance_origin:
                    min_distance_origin = float(origin.distance)
                    citie_origin_origin = origin.origin_city.name
                    destination_origin_city = origin.destination_city.name

            for destination in destinations:

                min_distance_destination = float(destinations[0].distance)

                citie_destination_origin = destinations[0].origin_city.name

                destination_destination_city = destinations[0].destination_city.name

                if float(destination.distance) < min_distance_destination:
                    min_distance_destination = float(destination.distance)
                    citie_destination_origin = destination.origin_city.name
                    destination_destination_city = destination.destination_city.name

            total_distance = __sum_total_distance(
                min_distance_origin, min_distance_destination)
            travel_cost = __calculate_travel_cost(
                total_distance, vehicle_autonomy, fuel_value)

            total_cities = [citie_origin_origin, destination_origin_city,
                            citie_destination_origin, destination_destination_city]
            lst_total_cities = (sorted(set(total_cities)))

            data = {
                'route': ' '.join(lst_total_cities),
                'cost': travel_cost
            }

            return JsonResponse(data, safe=False)
