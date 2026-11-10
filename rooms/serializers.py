"""TODO 1 — Implement a read-only Room ModelSerializer."""
from rest_framework import serializers
from rooms.models import Room

class RoomSerializer(serializers.ModelSerializer):
    # TODO 1 (5 points): add the related city field and Meta configuration.
    # Expose exactly code, name, capacity, location_city, all read-only.
    pass
