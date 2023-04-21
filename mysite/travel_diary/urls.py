from django.urls import path
from .views import *
from django.contrib.auth.views import PasswordResetView

app_name = 'travel'

urlpatterns = [
    path('', index, name='index'),
    path('destinations/', destinations, name='destinations'),
    path('destinations/<int:destination_id>', destination_entry, name='destination_entry'),
    path('user_destinations/', destination_list, name='user_destinations'),
    path('user_destinations/<int:destination_id>/', travelentry_list, name='travelentry_list'),
    path('create_destination/', create_destination, name='create_destination'),
    path('create_travel_entry/<int:destination_id>/', create_travel_entry, name='create_travel_entry'),
    path('search/', search, name='search'),
    path('register/', register, name='register'),
    path('destination/<int:pk>/delete/', destination_delete, name='destination_delete'),
    path('destination/<int:pk>/entry/<int:entry_pk>/delete/', travel_entry_delete, name='travelentry_delete'),
    path('destination/edit/<int:id>/', edit_destination, name='edit_destination'),
    path('destination/<int:destination_id>/entry/<int:entry_id>/edit/', edit_travel_entry, name='travelentry_edit'),
    # path('password-reset/', password_reset_confirm, name='password_reset'),

        
]