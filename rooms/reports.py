import json
from django.db.models import Sum
from .models import Location, Room


def export_city_summary(city: str) -> str:
    # 1. Validation de l'entrée
    if not isinstance(city, str) or not city.strip():
        raise ValueError("City must be a non-empty string.")

    cleaned_city = city.strip()

    # 2. Récupérer l'orthographe officielle depuis la base si connue
    location = Location.objects.filter(city__iexact=cleaned_city).first()
    display_city = location.city if location else cleaned_city

    # 3. Récupérer les salles triées par code
    rooms = Room.objects.filter(location__city__iexact=cleaned_city).order_by('code')

    # 4. Agréger les données
    room_codes = list(rooms.values_list('code', flat=True))
    total_rooms = rooms.count()
    total_capacity = rooms.aggregate(total=Sum('capacity'))['total'] or 0

    data = {
        "city": display_city,
        "total_rooms": total_rooms,
        "total_capacity": total_capacity,
        "room_codes": room_codes
    }

    return json.dumps(data)