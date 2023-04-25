from django import forms
from .models import Destination, TravelEntry
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


class DestinationForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label='Country', widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control'}))
    image = forms.ImageField(label='Add Image', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    class Meta:
        
        model = Destination
        fields = ('name', 'description', 'image')
        
   

class TravelEntryForm(forms.ModelForm):
    title = forms.CharField(max_length=200, label='Title', widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control'}))
    image = forms.ImageField(label='Add Image', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    destination = forms.ModelChoiceField(queryset=Destination.objects.all(), label='Country', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = TravelEntry
        fields = ('destination', 'title', 'text', 'image')
  



class UserUpdateForm(UserChangeForm):
    password = None
    username = forms.CharField(max_length=150, required=False, help_text='', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=150, required=False, help_text='', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    error_messages = {
        'username': {'invalid': "Enter a valid username."},
        'email': {'invalid': "Enter a valid email address."},
    }
    class Meta:
        model = User
        fields = ('username', 'email')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages.pop('required')
        self.fields['email'].error_messages.pop('required')
        



class PasswordChangeFormWithCheck(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

