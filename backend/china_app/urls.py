from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/provinces/', include('provinces.urls')),
    path('api/game/', include('game.urls')),
    path('api/quiz/', include('quiz.urls')),
    path('api/score/', include('score.urls')),
]
