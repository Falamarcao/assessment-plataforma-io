from rest_framework.viewsets import ModelViewSet
from .serializers import RoomSerializer
from .models import Room


class RoomViewSet(ModelViewSet):
    """
    API endpoint that allows...
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    # permission_classes = []
