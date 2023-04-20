from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import DestinationForm, TravelEntryForm
from django.contrib import messages
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import os

# Create your views here.

# NAVIGATION MENU
menu = [{'title': "Home", 'url_name': "travel:index"},
        {'title': "Entries", 'url_name': "travel:destinations"},
        {'title': "Add Your Destination", 'url_name': "travel:create_destination"}
        ]
# INDEX
def index(request):
    num_destinations = Destination.objects.count()
    num_travel_entries = TravelEntry.objects.count()
    image_names = os.listdir('media/destination_images')
    num_visists = request.session.get('num_visists',1)
    request.session['num_visists'] = num_visists + 1
    
    context = {
        'menu': menu,
        'title': 'Homepage',
        'title2': 'Share and explore travel stories',
        'num_destinations' : num_destinations,
        'num_travel_entries': num_travel_entries,
        'num_visists': num_visists,
        'image_names': image_names,
    }
    return render(request, 'travel_diary/index.html', context=context)


# LISTING ALL DESTINATIONS
@login_required
def destinations(request):
    data = Destination.objects.all()
    paginator = Paginator(data,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'menu': menu,
        'title': 'Travel entries',
        'title2': 'All travel entries',
        'page_obj' : page_obj
    }
    return render(request, 'travel_diary/destinations.html', context=context)

# SEARCH ALL DESTINATIONS
# old search
# @login_required
# def search(request):
#     query = request.GET.get('query')
#     if query:
#         search_results = Destination.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
#     else:
#         search_results = Destination.objects.all()
#     # pagination
#     paginator = Paginator(search_results, 3)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {
#         'menu': menu,
#         'title': 'Search results' if query else 'Travel entries',
#         'query': query,
#         'page_obj': page_obj,
#     }
#     return render(request, 'travel_diary/search.html', context)

@login_required
def search(request):
    query = request.GET.get('query')
    if query:
        destinations = Destination.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        entries = TravelEntry.objects.filter(destination__in=destinations)
    else:
        entries = TravelEntry.objects.all()
    # pagination
    paginator = Paginator(entries, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'menu': menu,
        'title': 'Search results' if query else 'Travel entries',
        'query': query,
        'page_obj': page_obj,
    }
    return render(request, 'travel_diary/search.html', context)


# TRAVEL ENTRY FOR SPECIFIC DESTINATION


@login_required
def destination_entry(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    query = request.GET.get('query')
    entries = destination.travelentry_set.all()
    if query:
        entries = entries.filter(title__icontains=query)
    context = {
        'destination': destination,
        'entries': entries,
        'menu': menu
    }
    return render(request, 'travel_diary/destination_entries.html', context=context)



# REGISTRATION
def register(request):
    context = {
        'menu': menu,
        'title': 'Registration',
        'title2': 'Register here'
    }
    return render(request, 'travel_diary/registration.html', context=context)

# USER PROFILE WHICH LISTS ALL USER ENTERED DESTINATION BY USING THAT SPECIFIC LOGGED-IN USER ID
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

# LISTS ALL TRAVEL ENTRIES FOR A DESTINATION, AGAIN ONLY FOR LOGGED IN USER BY USING LOGGED IN USER ID
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

# CREATE NEW DESTINATION
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

# CREATE TRAVEL ENTRY FOR THAT DESTINATION
@login_required
def create_travel_entry(request, destination_id):
    destination = Destination.objects.get(id=destination_id)
    if request.method == 'POST':
        form = TravelEntryForm(request.POST, request.FILES)
        if form.is_valid():
            travel_entry = form.save(commit=False)
            travel_entry.destination = destination
            travel_entry.save()
            messages.success(request, 'Travel entry added successfully.')
            return redirect('travel:destinations')
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

# REGISTRATION
@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password != password2:
            messages.error(request, 'Password mismatch!')
            return redirect('travel:register')
        try:
            validate_password(password)
        except ValidationError as e:
            for error in e:
                messages.error(request, error)
            return redirect('travel:register')
        # CHECK IF USERNAME ALREADY EXISTS
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username {username} already exists.')
            return redirect('travel:register')
        # CHECK IF EMAIL ALREADY EXISTS 
        if User.objects.filter(email=email).exists():
            messages.error(request, f'Email {email} is already in use. Please choose another.')
            return redirect('travel:register')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Registration successful! You can now login.')
        return redirect(reverse('login'))
    
    return render(request, 'travel_diary/register.html')

# DELETE DESTINATION
@login_required
def destination_delete(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        destination.delete()
        messages.success(request, f"Destination '{destination.name}' has been deleted.")
        return redirect('travel:user_destinations')
    else:
        messages.warning(request, "Deletion cancelled.")
        return redirect('travel:user_destinations')
    
# DELETE DESTINATION ENTRY
@login_required
def travel_entry_delete(request, pk, entry_pk):
    entry = get_object_or_404(TravelEntry, pk=entry_pk)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, f"Travel Entry '{entry.title}' has been deleted.")
        return redirect('travel:travelentry_list', destination_id=pk)
    else:
        messages.warning(request, "Deletion cancelled.")
        return redirect('travel:travelentry_list')

# EDIT DESTINATION 
@login_required
def edit_destination(request, id):
    destination = get_object_or_404(Destination, id=id, user=request.user)
    if request.method == 'POST':
        form = DestinationForm(request.POST, instance=destination)
        if form.is_valid():
            form.save()
            messages.success(request, f"Destination '{destination.name}' has been updated.")
            return redirect('travel:user_destinations')
    else:
        form = DestinationForm(instance=destination)
    context = {
        'menu': menu,
        'title': f'Edit destination: {destination.name}',
        'title2': f'Edit destination: {destination.name}',
        'form': form,
    }
    return render(request, 'travel_diary/edit_destination.html', context=context)

# EDIT DESTINATION ENTRY
@login_required
def edit_travel_entry(request, destination_id, entry_id):
    destination = get_object_or_404(Destination, id=destination_id, user=request.user)
    entry = get_object_or_404(TravelEntry, id=entry_id, destination=destination)
    if request.method == 'POST':
        form = TravelEntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, f"Travel Entry '{entry.title}' has been updated.")
            return redirect('travel:travelentry_list', destination_id=destination_id)
    else:
        form = TravelEntryForm(instance=entry)
    context = {
        'menu': menu,
        'title': f'Edit entry: {entry.title}',
        'title2': f'Edit entry: {entry.title}',
        'form': form,
    }
    return render(request, 'travel_diary/edit_travel_entry.html', context=context)
