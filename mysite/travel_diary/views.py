from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

menu = [{'title': "Home", 'url_name': "index"},
        {'title': "Registration", 'url_name': "register"},
        {'title': "Login", 'url_name': "login"},
        
        ]

def index(request):
    context = {
        'menu': menu,
        'title': 'Homepage',
        'title2': 'Share and explore travel stories'
    }
    return render(request, 'travel_diary/index.html', context=context)

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