from django.contrib import admin
from django.contrib import admin
from .models import Destination, TravelEntry
# Register your models here.



class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')

class TravelEntryAdmin(admin.ModelAdmin):
    # list_display = ('title', 'destination', 'user', 'created_at', 'updated_at')
    list_display = ('title', 'destination', 'created_at', 'updated_at')
    # list_filter = ('destination', 'user', 'created_at')
    list_filter = ('destination', 'created_at')
    
    search_fields = ('title', 'text')

admin.site.register(Destination, DestinationAdmin)
admin.site.register(TravelEntry, TravelEntryAdmin)
