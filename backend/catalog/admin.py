from django.contrib import admin
from .models import Category, Service, ServiceRequest

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration_minutes', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name',)

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'service', 'phone', 'desired_at', 'status')
    list_filter = ('status',)
