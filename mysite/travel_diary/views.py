from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

menu = [{'title': "Home", 'url_name': "index"},
        
        ]

def index(request):
    context = {
        'menu': menu,
        'title': 'Homepage',
        'title2': 'Share and explore travel stories'
    }
    return render(request, 'travel_diary/index.html', context=context)