from django.urls import path
from .views import *

app_name = 'travel'

urlpatterns = [
    path('', index, name='index'),
    path('destinations/', destinations, name='destinations'),
    path('destinations/<int:destination_id>', destination_entry, name='destination_entry'),
    path('user_destinations/', destination_list, name='user_destinations'),
    path('user_destinations/<int:destination_id>/', travelentry_list, name='travelentry_list'),
    path('create_destination/', create_destination, name='create_destination'),
    path('create_travel_entry/', create_travel_entry, name='create_travel_entry'),
 
    
    
]