from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Room
from .serializers import RoomSerializer


class RoomListView(APIView):
    """
    GET /api/rooms/
    Retourne la liste des salles en lecture seule.
    """

    def get(self, request):
        queryset = Room.objects.select_related('location').order_by('code')

        if 'city' in request.query_params:
            city_param = request.query_params.get('city')
            cleaned_city = city_param.strip() if city_param else ''

            if not cleaned_city:
                return Response(
                    {"error": "City parameter cannot be blank."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            queryset = queryset.filter(location__city__iexact=cleaned_city)

        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)