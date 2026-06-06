from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizQuestionViewSet, QuizResultViewSet

router = DefaultRouter()
router.register(r'questions', QuizQuestionViewSet)
router.register(r'results', QuizResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
