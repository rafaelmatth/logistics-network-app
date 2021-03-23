from django.urls import path, include
from .views import CreateMap, HandleLogisticsNetwork, GetTravelValue, TotalRoutesCity

urlpatterns = [
    path('create/map', CreateMap.as_view()),
    
    path('logistics_network', HandleLogisticsNetwork.as_view()),

    path('get_travel_value', GetTravelValue.as_view()),

    path('total_routes_city', TotalRoutesCity.as_view()),
]
