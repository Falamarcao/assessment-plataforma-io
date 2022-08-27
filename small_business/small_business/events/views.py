from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

from .serializers import EventSerializer
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
        start_at = str_to_datetime(self.request.query_params.get('start_at'))
        end_at = str_to_datetime(self.request.query_params.get('end_at'), True)

        if start_at and end_at:
            self.queryset = self.queryset.filter(start_at__range=(start_at, end_at))
        elif start_at:
            self.queryset = self.queryset.filter(start_at__gte=start_at)
        # ------------ #

        # Filtering queryset for customers - "They can see only public or their own"
        groups = self.request.user.groups.values_list('name', flat=True)
        if 'customers' in groups:
            self.queryset = self.queryset.filter(Q(owner=self.request.user.id) | Q(event_type='public'))

        return self.queryset.order_by('start_at')

    def destroy(self, request, *args, **kwargs):
        groups = self.request.user.groups.values_list('name', flat=True)
        if 'customers' in groups:
            instance = self.get_object()
            if instance.owner.id != request.user.id:
                return Response("Customers can only cancel their own events.", status.HTTP_401_UNAUTHORIZED)

        return super(EventViewSet, self).destroy(request, *args, **kwargs)
