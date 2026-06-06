from rest_framework import serializers
from .models import Province, Region, QuizQuestion


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']


class ProvinceListSerializer(serializers.ModelSerializer):
    """省份列表序列化器（轻量）"""
    region_name = serializers.CharField(source='region.name', read_only=True, default='')

    class Meta:
        model = Province
        fields = [
            'id', 'name', 'capital', 'abbr', 'feature',
            'emoji', 'region_name', 'image', 'visited_count',
        ]


class ProvinceDetailSerializer(serializers.ModelSerializer):
    """省份详情序列化器"""
    region_name = serializers.CharField(source='region.name', read_only=True, default='')

    class Meta:
        model = Province
        fields = [
            'id', 'name', 'capital', 'abbr', 'feature', 'emoji',
            'region_name', 'fun_fact', 'description', 'image',
            'visited_count',
        ]


class QuizQuestionSerializer(serializers.ModelSerializer):
    province_name = serializers.CharField(source='province.name', read_only=True)

    class Meta:
        model = QuizQuestion
        fields = [
            'id', 'province', 'province_name', 'question_type',
            'question_text', 'correct_answer', 'option_a',
            'option_b', 'option_c', 'option_d',
        ]
