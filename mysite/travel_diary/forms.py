from django import forms
from .models import Destination, TravelEntry

class DestinationForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label='Destination Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control'}))
    image = forms.ImageField(label='Add Image', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    class Meta:
        
        model = Destination
        fields = ('name', 'description', 'image')
        
   

class TravelEntryForm(forms.ModelForm):
    title = forms.CharField(max_length=200, label='Title', widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control'}))
    image = forms.ImageField(label='Add Image', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    destination = forms.ModelChoiceField(queryset=Destination.objects.all(), label='Destination', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = TravelEntry
        fields = ('destination', 'title', 'text', 'image')
  