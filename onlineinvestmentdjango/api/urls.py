from django.urls import path, include
from .views import multithreading_calculate_land_values, retrieve_land_values

urlpatterns = [
    path('updateLandValues/', multithreading_calculate_land_values),
    path('getLandValues/', retrieve_land_values)
]