from django.urls import path
from .views import *

app_name = 'travel'

urlpatterns = [
    path('', index, name='index'),
    path('destinations/', destinations, name='destinations'),
    path('destinations/<int:destination_id>', destination_entry, name='destination_entry'),
    path('user_destinations/', destination_list, name='user_destinations'),
    path('destinations/<int:pk>/travel_entries/', travelentry_list, name='travelentry_list'),
 
    
    
]