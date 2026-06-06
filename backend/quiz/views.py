from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import QuizQuestion, QuizResult
from .serializers import QuizQuestionSerializer, QuizResultSerializer
import random

class QuizQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializer

    @action(detail=False, methods=['get'])
    def random(self, request):
        count = int(request.query_params.get('count', 10))
        questions = list(self.queryset.all())
        random.shuffle(questions)
        selected = questions[:count]
        serializer = self.get_serializer(selected, many=True)
        return Response(serializer.data)

class QuizResultViewSet(viewsets.ModelViewSet):
    queryset = QuizResult.objects.all()
    serializer_class = QuizResultSerializer
