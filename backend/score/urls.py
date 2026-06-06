from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserScoreViewSet

router = DefaultRouter()
router.register(r'', UserScoreViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
