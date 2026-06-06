from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import UserScore
from .serializers import UserScoreSerializer

class UserScoreViewSet(viewsets.ModelViewSet):
    queryset = UserScore.objects.all()
    serializer_class = UserScoreSerializer

    @action(detail=False, methods=['post'])
    def visit(self, request):
        user_id = request.data.get('user_id')
        province_name = request.data.get('province_name')
        
        try:
            score_obj = UserScore.objects.get(user_id=user_id)
        except UserScore.DoesNotExist:
            score_obj = UserScore.objects.create(user_id=user_id)
        
        if province_name not in score_obj.visited_provinces:
            score_obj.visited_provinces.append(province_name)
            score_obj.score += 10
            self.check_badges(score_obj)
            score_obj.save()
        
        serializer = self.get_serializer(score_obj)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_score(self, request):
        user_id = request.data.get('user_id')
        points = request.data.get('points', 0)
        
        try:
            score_obj = UserScore.objects.get(user_id=user_id)
        except UserScore.DoesNotExist:
            score_obj = UserScore.objects.create(user_id=user_id)
        
        score_obj.score += points
        self.check_badges(score_obj)
        score_obj.save()
        
        serializer = self.get_serializer(score_obj)
        return Response(serializer.data)

    def check_badges(self, score_obj):
        badges = score_obj.badges
        visited_count = len(score_obj.visited_provinces)
        score = score_obj.score
        
        if visited_count >= 1 and 'first' not in badges:
            badges.append('first')
        if visited_count >= 10 and 'explorer' not in badges:
            badges.append('explorer')
        if visited_count >= 34 and 'all' not in badges:
            badges.append('all')
        if score >= 100 and 'score100' not in badges:
            badges.append('score100')
        if score >= 500 and 'score500' not in badges:
            badges.append('score500')
        
        score_obj.badges = badges
