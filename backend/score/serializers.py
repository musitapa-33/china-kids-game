from rest_framework import serializers
from .models import UserScore

class UserScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserScore
        fields = ['id', 'user_id', 'score', 'visited_provinces', 'badges', 'created_at', 'updated_at']
