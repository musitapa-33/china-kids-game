from rest_framework import viewsets
from .models import Province
from .serializers import ProvinceSerializer

class ProvinceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

    def get_queryset(self):
        queryset = Province.objects.all()
        region = self.request.query_params.get('region')
        if region:
            queryset = queryset.filter(region=region)
        return queryset
