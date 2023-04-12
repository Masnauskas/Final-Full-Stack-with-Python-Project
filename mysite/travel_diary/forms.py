from django import forms
from .models import Destination, TravelEntry

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ('name', 'description', 'image')

class TravelEntryForm(forms.ModelForm):
    class Meta:
        model = TravelEntry
        fields = ('destination','title', 'text', 'image' )
        # widgets = {
        #     'destination': forms.HiddenInput(),
        # }
    # def __init__(self, *args, destination_id=None, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if destination_id:
    #         self.fields['destination'].initial = Destination.objects.get(id=destination_id)
        
  