from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.

menu = [{'title': "Home", 'url_name': "travel:index"},
        {'title': "Entries", 'url_name': "travel:destinations"},
        {'title': "Registration", 'url_name': "travel:register"},
        {'title': "Login", 'url_name': "travel:login"},
        
        ]

def index(request):
    context = {
        'menu': menu,
        'title': 'Homepage',
        'title2': 'Share and explore travel stories'
    }
    return render(request, 'travel_diary/index.html', context=context)

def destinations(request):
    data = Destination.objects.all()
    context = {
        'menu': menu,
        'title': 'Travel entries',
        'title2': 'All travel entries',
        'data': data
    }
    return render(request, 'travel_diary/destinations.html', context=context)

def destination_entry(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    entries = destination.travelentry_set.all()
    context = {
        'destination': destination,
        'entries': entries,
        'menu': menu
    }
    return render(request, 'travel_diary/destination_entries.html', context=context)

def register(request):
    context = {
        'menu': menu,
        'title': 'Registration',
        'title2': 'Register here'
    }
    return render(request, 'travel_diary/registration.html', context=context)

def login(request):
    context = {
        'menu': menu,
        'title': 'Login',
        'title2': 'Login'
    }
    return render(request, 'travel_diary/login.html', context=context)