from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PuzzleProgressViewSet

router = DefaultRouter()
router.register(r'puzzle', PuzzleProgressViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
