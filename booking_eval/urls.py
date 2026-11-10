from django.urls import path
from rooms.views import RoomListView
from rooms.web_views import room_catalogue

urlpatterns = [
    path('rooms/', room_catalogue, name='room-catalogue'),
    path('api/rooms/', RoomListView.as_view(), name='room-list'),
]
