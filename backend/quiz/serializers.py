from rest_framework import serializers
from .models import QuizQuestion, QuizResult

class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = ['id', 'question', 'choices', 'answer', 'question_type', 'province_id']

class QuizResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizResult
        fields = ['id', 'user_id', 'score', 'total_questions', 'correct_count', 'created_at']
