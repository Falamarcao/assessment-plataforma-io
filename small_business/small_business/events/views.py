from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from .serializers import EventSerializer
from django.db.models import Q

from .utils import str_to_datetime
from .models import Event


class EventStandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 20
    page_query_param = 'p'


class EventViewSet(ModelViewSet):
    """
    The business can create a room with M capacity.
    The business can delete a room if said room does not have any events.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = EventStandardResultsSetPagination

    # permission_classes = []

    def get_queryset(self):

        # Optional query parameters - "Search by date range"
        start_at = str_to_datetime(self.request.query_params.get('start_date'))
        end_at = str_to_datetime(self.request.query_params.get('end_date'), True)

        if start_at and end_at:
            self.queryset = self.queryset.filter(start_at__range=(start_at, end_at))
        elif start_at:
            self.queryset = self.queryset.filter(end_at__gte=start_at)
        # ------------ #

        # Filtering queryset for customers - "They can see only public or their own"
        groups = self.request.user.groups.all()
        if 'customer' in groups:
            self.queryset = self.get_queryset().filter(Q(event_type='public') | Q(owner=self.request.user.id))

        return self.queryset
