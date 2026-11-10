"""TODO 3 — Export a city catalogue summary as a JSON string."""
import json
from rooms.models import Location, Room

def export_city_summary(city: str) -> str:
    """Return JSON containing city, total_rooms, total_capacity, room_codes."""
    # TODO 3 (5 points): validate city, query Room/Location, aggregate and
    # return json.dumps(...). Do not hard-code fixture results.
    raise NotImplementedError('TODO 3: implement city JSON report')
