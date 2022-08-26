from rest_framework.routers import SimpleRouter
from .views import RoomViewSet
from django.urls import path

app_name = 'rooms'

router = SimpleRouter()
router.register(r'rooms', RoomViewSet, basename='rooms')
