from django.urls import path, include
from .views import CreateMap, CreateLogisticNetwork, GetTravelValue

urlpatterns = [
    path('create/map', CreateMap.as_view()),
    path('create/logistic_network', CreateLogisticNetwork.as_view()),
    path('get_travel_value', GetTravelValue.as_view()),
]
