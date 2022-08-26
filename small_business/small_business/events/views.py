from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import EventSerializer
from .models import Event


class EventViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows...
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # permission_classes = []
