from rest_framework import viewsets
from .models import PuzzleProgress
from .serializers import PuzzleProgressSerializer

class PuzzleProgressViewSet(viewsets.ModelViewSet):
    queryset = PuzzleProgress.objects.all()
    serializer_class = PuzzleProgressSerializer
