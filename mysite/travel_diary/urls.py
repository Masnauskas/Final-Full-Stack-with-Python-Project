from django.urls import path
from .views import *

app_name = 'travel'

urlpatterns = [
    path('', index, name='index'),
    path('destinations/', destinations, name='destinations'),
    path('destinations/<int:destination_id>', destination_entry, name='destination_entry'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
]