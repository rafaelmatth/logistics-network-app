from django.urls import path, include
from .views import CreateMap

urlpatterns = [
    path('create_map', CreateMap.as_view()),
]
