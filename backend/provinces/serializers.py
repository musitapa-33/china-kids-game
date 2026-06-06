from rest_framework import serializers
from .models import Province, ProvinceImage

class ProvinceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvinceImage
        fields = ['id', 'file_path', 'caption', 'is_png']

class ProvinceSerializer(serializers.ModelSerializer):
    images = ProvinceImageSerializer(many=True, read_only=True)

    class Meta:
        model = Province
        fields = ['id', 'name', 'abbr', 'capital', 'region', 'emoji', 'features', 'fact', 'images']
