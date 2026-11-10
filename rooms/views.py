"""TODO 2 — Read-only rooms endpoint with an optional city filter."""
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rooms.models import Room
from rooms.serializers import RoomSerializer

class RoomListView(generics.ListAPIView):
    serializer_class = RoomSerializer
    queryset = Room.objects.none()  # TODO: replace with the actual catalogue

    def get_queryset(self):
        # TODO 2 (6 points): order by code, optionally filter city.
        # Trim/ignore case; blank supplied city -> HTTP 400.
        # Do not expose write methods.
        return super().get_queryset()
