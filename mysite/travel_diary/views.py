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

def search(request):
    query = request.GET.get('query')
    if query:
        search_results = Destination.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        search_results = Destination.objects.all()
    paginator = Paginator(search_results, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'menu': menu,
        'title': 'Search results' if query else 'Travel entries',
        'query': query,
        'page_obj': page_obj,
    }
    return render(request, 'travel_diary/search.html', context)

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

# def login(request):
#     context = {
#         'menu': menu,
#         'title': 'Login',
#         'title2': 'Login'
#     }
#     return render(request, 'travel_diary/login.html', context=context)


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

        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username {username} already exists.')
            return redirect('travel:register')
                
        if User.objects.filter(email=email).exists():
            messages.error(request, f'Email {email} is already in use. Please choose another.')
            return redirect('travel:register')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Registration successful! You can now login.')
        return redirect(reverse('login'))
    
    return render(request, 'travel_diary/register.html')

# DELETE destination
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
    
# DELETE destination entry
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
    
