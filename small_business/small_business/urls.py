"""small_business URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.routers import DefaultRouter
from django.views.generic import RedirectView
from django.urls import path, include
from django.contrib import admin

from .users.urls import router as users_router
from .rooms.urls import router as rooms_router
from .events.urls import router as events_router


router = DefaultRouter()
router.registry.extend(users_router.registry)
router.registry.extend(rooms_router.registry)
router.registry.extend(events_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include(router.urls)),

    # Redirect just for exemplification
    path('', RedirectView.as_view(url='api/v1/', permanent=False), name='home'),
]
