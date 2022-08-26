from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import RoomSerializer
from .models import Room


class RoomViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows...
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    # permission_classes = []
