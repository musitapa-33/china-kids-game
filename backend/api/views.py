import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch
from .models import Province, Region, QuizQuestion
from .serializers import (
    ProvinceListSerializer, ProvinceDetailSerializer,
    RegionSerializer, QuizQuestionSerializer,
)


@api_view(['GET'])
def health_check(request):
    """健康检查"""
    return Response({'status': 'ok', 'service': 'china-app-api'})


@api_view(['GET'])
def province_list(request):
    """省份列表"""
    region = request.query_params.get('region')
    queryset = Province.objects.select_related('region').all()
    if region:
        queryset = queryset.filter(region__name=region)
    serializer = ProvinceListSerializer(queryset, many=True)
    return Response({'data': serializer.data})


@api_view(['GET'])
def province_detail(request, pk):
    """省份详情"""
    try:
        province = Province.objects.select_related('region').get(pk=pk)
    except Province.DoesNotExist:
        return Response({'error': '省份不存在'}, status=status.HTTP_404_NOT_FOUND)
    # 尝试增加访问计数，失败不影响正常返回
    try:
        province.visited_count += 1
        province.save(update_fields=['visited_count'])
    except Exception:
        pass
    serializer = ProvinceDetailSerializer(province)
    return Response({'data': serializer.data})


@api_view(['GET'])
def region_list(request):
    """区域列表"""
    regions = Region.objects.all()
    serializer = RegionSerializer(regions, many=True)
    return Response({'data': serializer.data})


@api_view(['GET'])
def quiz_questions(request):
    """获取答题题目"""
    count = int(request.query_params.get('count', 10))
    questions = list(QuizQuestion.objects.select_related('province').all())
    selected = random.sample(questions, min(count, len(questions)))
    serializer = QuizQuestionSerializer(selected, many=True)
    return Response({'data': serializer.data})


@api_view(['GET'])
def matching_data(request):
    """获取匹配游戏数据"""
    mode = request.query_params.get('mode', 'capital')
    provinces = Province.objects.all()
    data = []
    for p in provinces:
        if mode == 'capital':
            data.append({'name': p.name, 'match': p.capital})
        elif mode == 'abbr':
            data.append({'name': p.name, 'match': p.abbr})
        elif mode == 'feature':
            data.append({'name': p.name, 'match': p.feature})
    random.shuffle(data)
    return Response({'data': data, 'mode': mode})


@api_view(['GET'])
def puzzle_data(request):
    """获取拼图游戏数据"""
    provinces = Province.objects.all().values('id', 'name', 'emoji')
    return Response({'data': list(provinces)})


@api_view(['GET'])
def gallery_data(request):
    """获取图片浏览数据"""
    provinces = Province.objects.select_related('region').all()
    result = []
    for p in provinces:
        result.append({
            'id': p.id,
            'name': p.name,
            'emoji': p.emoji,
            'region_name': p.region.name if p.region else '',
            'image': p.image,
            'capital': p.capital,
            'abbr': p.abbr,
            'feature': p.feature,
        })
    return Response({'data': result})
