from django.urls import path, include
from .views import CreateMap, CreateLogisticNetwork, GetTravelValue, ListLogisticNetwork

urlpatterns = [
    path('create/map', CreateMap.as_view()),
    
    path('create/logistics_network', CreateLogisticNetwork.as_view()),
    path('list/logistics_network', ListLogisticNetwork.as_view()),

    path('get_travel_value', GetTravelValue.as_view()),
]
