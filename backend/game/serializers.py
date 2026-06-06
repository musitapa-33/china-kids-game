from rest_framework import serializers
from .models import PuzzleProgress

class PuzzleProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuzzleProgress
        fields = ['id', 'user_id', 'difficulty', 'completed', 'correct_count', 'total_count', 'created_at', 'updated_at']
