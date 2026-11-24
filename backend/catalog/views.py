from datetime import timedelta
from django.db.models import Count
from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import Category, Service, ServiceRequest
from .serializers import CategorySerializer, ServiceSerializer, ServiceRequestSerializer

class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or bool(request.user and request.user.is_staff)

class ServiceFilter(filters.FilterSet):
    category = filters.NumberFilter(field_name='category_id')
    is_available = filters.TypedChoiceFilter(choices=(('true', 'true'), ('false', 'false')), coerce=lambda v: v == 'true')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    class Meta:
        model = Service
        fields = ('category', 'is_available', 'min_price', 'max_price')

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [AdminOrReadOnly]

    @action(detail=True, methods=['get'])
    def services(self, request, pk=None):
        category = self.get_object()
        queryset = Service.objects.select_related('category').filter(category=category)
        if not request.user.is_staff:
            queryset = queryset.filter(is_available=True)
        queryset = ServiceFilter(request.query_params, queryset=queryset.order_by('id'))
        if not queryset.is_valid():
            from rest_framework.exceptions import ValidationError
            raise ValidationError(queryset.errors)
        page = self.paginate_queryset(queryset.qs)
        return self.get_paginated_response(ServiceSerializer(page, many=True).data)

class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [AdminOrReadOnly]
    filterset_class = ServiceFilter
    search_fields = ('name', 'description')
    ordering_fields = ('price',)

    def get_queryset(self):
        qs = Service.objects.select_related('category').order_by('id')
        return qs if self.request.user.is_staff else qs.filter(is_available=True)

class ServiceRequestViewSet(viewsets.ModelViewSet):
    queryset = ServiceRequest.objects.select_related('service').order_by('id')
    serializer_class = ServiceRequestSerializer

    def get_permissions(self):
        return [permissions.AllowAny()] if self.action == 'create' else [permissions.IsAdminUser()]

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def statistics(request):
    today = timezone.localdate()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=7)
    return Response({
        'services_by_category': list(Category.objects.annotate(service_count=Count('services')).values('id', 'name', 'service_count').order_by('id')),
        'new_requests_this_week': ServiceRequest.objects.filter(status=ServiceRequest.Status.NEW, created_at__date__gte=start, created_at__date__lt=end).count(),
    })
