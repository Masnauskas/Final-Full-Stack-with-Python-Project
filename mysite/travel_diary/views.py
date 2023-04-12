from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import DestinationForm, TravelEntryForm
from django.contrib import messages


# Create your views here.

menu = [{'title': "Home", 'url_name': "travel:index"},
        {'title': "Entries", 'url_name': "travel:destinations"},
        {'title': "Add Your Destination", 'url_name': "travel:create_destination"}
        
        
        ]

def index(request):
    num_destinations = Destination.objects.count()
    num_travel_entries = TravelEntry.objects.count()
    
    num_visists = request.session.get('num_visists',1)
    request.session['num_visists'] = num_visists + 1
    
    context = {
        'menu': menu,
        'title': 'Homepage',
        'title2': 'Share and explore travel stories',
        'num_destinations' : num_destinations,
        'num_travel_entries': num_travel_entries,
        'num_visists': num_visists
    }
    return render(request, 'travel_diary/index.html', context=context)



def destinations(request):
    query = request.GET.get('q')
    if query:
        data = Destination.objects.filter(Q(name__icontains=query))
    else:
        data = Destination.objects.all()
    paginator = Paginator(data,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'menu': menu,
        'title': 'Travel entries',
        'title2': 'All travel entries',
        'data': data,
        'page_obj' : page_obj
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


@login_required
def destination_list(request):
    destinations = Destination.objects.filter(user=request.user)
    context = {
        'menu': menu,
        'title': 'Your destinations',
        'title2': 'Your destinations',
        'destinations': destinations
    }
    
    return render(request, 'travel_diary/destination_list.html', context=context)

@login_required
def travelentry_list(request, destination_id):
    
    destination = get_object_or_404(Destination, id=destination_id, user=request.user)
    entries = destination.travelentry_set.all()
    context = {
        'menu': menu,
        'title': 'Travel entries',
        'title2': 'Travel entries',
        'destination': destination,
        'entries': entries
    }
    
    return render(request, 'travel_diary/travelentry_list.html', context=context)

@login_required
def create_destination(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            
            destination = form.save(commit=False)
            destination.user = request.user
            destination.save()
            messages.success(request, 'Destination created successfully!')
            return redirect('travel:create_travel_entry', destination_id=destination.id)
            
    else:
        form = DestinationForm()
    context = {
        'menu': menu,
        'title': 'Add destination',
        'title2': 'Add destination',
        'form': form
        
    }
    return render(request, 'travel_diary/create_destination.html', context=context)


@login_required
def create_travel_entry(request, destination_id):
    destination = Destination.objects.get(id=destination_id)
    if request.method == 'POST':
        form = TravelEntryForm(request.POST, request.FILES, destination_id=destination_id)
        if form.is_valid():
            travel_entry = form.save(commit=False)
            travel_entry.destination = destination
            travel_entry.save()
            messages.success(request, 'Travel entry added successfully.')
            return redirect('travel:destinations', destination_id=destination_id)
    else:
        form = TravelEntryForm()
    context = {
        'menu': menu,
        'title': 'Add entry',
        'title2': 'Add entry',
        'form': form,
        'destination': destination
        
    }
    return render(request, 'travel_diary/create_travel_entry.html', context=context)