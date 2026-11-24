from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from catalog.views import CategoryViewSet, ServiceViewSet, ServiceRequestViewSet, statistics

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('services', ServiceViewSet, basename='service')
router.register('requests', ServiceRequestViewSet)
urlpatterns = [path('admin/', admin.site.urls), path('api/statistics/', statistics), path('api/', include(router.urls)), path('api-auth/', include('rest_framework.urls'))]
