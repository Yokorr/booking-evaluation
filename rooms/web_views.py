"""Supplied M4 example: ORM queryset passed to a Django template."""
from django.shortcuts import render
from rooms.models import Room


def room_catalogue(request):
    rooms = Room.objects.select_related('location').order_by('code')
    return render(request, 'rooms/catalogue.html', {'rooms': rooms})
