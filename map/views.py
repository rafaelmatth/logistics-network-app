from django.shortcuts import render

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.http import JsonResponse, request
from .models import Map, LogisticsNetwork, Cities, HistoryLogisticNetwork

import json
import re

class CreateMap(APIView):
    permission_classes = [IsAuthenticated]
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


class HandleLogisticsNetwork(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        maps = Map.objects.all()
        logistics_network = LogisticsNetwork.objects.all()

        response_data = []
        for map_data in maps:
            data = {
                'id': map_data.id,
                'map_name': map_data.name,
                'logistics_network': []
            }

            for logistic_network in logistics_network:
                logistic_data = {
                    'id': logistic_network.id,
                    'origin_city':  logistic_network.origin_city.name,
                    'destination_city':  logistic_network.destination_city.name,
                    'distance  ':  logistic_network.distance
                }

                data['logistics_network'].append(logistic_data)

            response_data.append(data)

        return JsonResponse(response_data, safe=False)

    def post(self, request):
        '''Post method to create a new map, always required the name'''
        req_post = json.loads(request.body)
        try:
            map_name = str(req_post['map_name'])
            origin_city = str(req_post['origin_city'])
            destination_city = str(req_post['destination_city'])
            distance = float(req_post['distance'])

            if(bool(re.search('\D', origin_city)) == False or bool(re.search('\D', destination_city)) == False):
                return JsonResponse(status=406, data={'message': 'invalid destination or origin city name'})
        except:
            return JsonResponse(status=406, data={'message': 'wrong data format'})

        '''Check that the names of the cities of origin and destination are the same'''
        if origin_city == destination_city:
            return JsonResponse(status=406, data={'message': 'name of city of origin and destination cannot be the same'})

        '''Method to create or call an object of the city model'''
        get_origin_city = Cities.objects.get_or_create(name=origin_city)[0]
        get_destination_city = Cities.objects.get_or_create(name=destination_city)[0]

        '''Check if the map exists and register a new logistics network'''
        try:
            get_map = Map.objects.get(name=map_name)

            new_logistic_network = LogisticsNetwork.objects.create(
                map_network=get_map, origin_city=get_origin_city, destination_city=get_destination_city, distance=distance)

            new_logistic_network.save()

            new_log_history = HistoryLogisticNetwork.objects.create(logistic_network=new_logistic_network, user=request.user)
            new_log_history.save()
            
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
    
    def delete(self, request):
        req_delete = json.loads(request.body)
        try:
            logistic_network = LogisticsNetwork.objects.get(id=req_delete['id'])
            logistic_network.delete()
            return Response(data={'message': 'logistic network successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data={'message': 'logistic network not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        req_put = json.loads(request.body)
        try:
            id_logistic_network = int(req_put['id'])
            origin_city = str(req_put['origin_city'])
            destination_city = str(req_put['destination_city'])
            distance = float(req_put['distance'])

            get_origin_city = Cities.objects.get_or_create(name=origin_city)[0]
            get_destination_city = Cities.objects.get_or_create(name=destination_city)[0]
            
            logistic_network = LogisticsNetwork.objects.get(id=id_logistic_network)

            logistic_network.origin_city = get_origin_city
            logistic_network.destination_city = get_destination_city
            logistic_network.distance = distance
            logistic_network.save()

            return JsonResponse(status=200, data={'message': 'logistical network updated successfully'})

        except:
            return Response(data={'message': 'invalid request data'}, status=status.HTTP_400_BAD_REQUEST)
        
class GetTravelValue(APIView):
    permission_classes = [IsAuthenticated]
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

class TotalRoutesCity(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        req_post = json.loads(request.body)
        try:
            city = str(req_post['city_name'])
            get_city = Cities.objects.get(name=city)
            records_of_origins = LogisticsNetwork.objects.filter(origin_city=get_city).count()
            records_of_destinations = LogisticsNetwork.objects.filter(destination_city=get_city).count()

            total_records = records_of_origins + records_of_destinations

            response_data = {
                'city_name': city,
                'total_routes': total_records
            }

            return Response(data=response_data, status=status.HTTP_200_OK)

        except:
            return Response(data={'message': 'city name not found'}, status=status.HTTP_400_BAD_REQUEST)