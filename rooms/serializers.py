from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    location_city = serializers.CharField(source='location.city', read_only=True)

    class Meta:
        model = Room
        fields = ['code', 'name', 'capacity', 'location_city']
        read_only_fields = ['code', 'name', 'capacity', 'location_city']