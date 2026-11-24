from django.utils import timezone
from rest_framework import serializers
from .models import Category, Service, ServiceRequest

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ('created_at',)

class ServiceRequestSerializer(serializers.ModelSerializer):
    service_id = serializers.PrimaryKeyRelatedField(source='service', queryset=Service.objects.all())
    class Meta:
        model = ServiceRequest
        fields = ('id', 'service_id', 'client_name', 'phone', 'desired_at', 'status', 'created_at')
        read_only_fields = ('status', 'created_at')

    def validate_service_id(self, service):
        if not service.is_available:
            raise serializers.ValidationError('Услуга недоступна.')
        return service

    def validate_desired_at(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError('Укажите будущую дату.')
        return value

    def validate_phone(self, value):
        if not value.strip():
            raise serializers.ValidationError('Укажите телефон.')
        return value.strip()
