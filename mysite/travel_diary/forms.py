from django import forms
from .models import Destination, TravelEntry

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ('name', 'description', 'image')

class TravelEntryForm(forms.ModelForm):
    class Meta:
        model = TravelEntry
        fields = ('destination', 'title', 'text', 'image' )