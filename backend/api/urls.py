from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health'),
    path('provinces/', views.province_list, name='province-list'),
    path('provinces/<int:pk>/', views.province_detail, name='province-detail'),
    path('regions/', views.region_list, name='region-list'),
    path('quiz/', views.quiz_questions, name='quiz-questions'),
    path('matching/', views.matching_data, name='matching-data'),
    path('puzzle/', views.puzzle_data, name='puzzle-data'),
    path('gallery/', views.gallery_data, name='gallery-data'),
]
