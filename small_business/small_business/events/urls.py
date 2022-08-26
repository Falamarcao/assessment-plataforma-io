from rest_framework.routers import SimpleRouter
from .views import EventViewSet
from django.urls import path

app_name = 'events'

router = SimpleRouter()
router.register(r'events', EventViewSet, basename='events')
