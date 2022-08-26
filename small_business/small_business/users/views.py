from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import UserSerializer
from .models import User


class UserViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows...
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = []
