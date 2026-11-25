from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from catalog.views import CategoryViewSet, ServiceViewSet, ServiceRequestViewSet, statistics
from catalog.auth_views import session_info, login_view, logout_view

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('services', ServiceViewSet, basename='service')
router.register('requests', ServiceRequestViewSet)
urlpatterns = [path('api/session/', session_info), path('api/login/', login_view), path('api/logout/', logout_view), path('admin/', admin.site.urls), path('api/statistics/', statistics), path('api/', include(router.urls)), path('api-auth/', include('rest_framework.urls'))]
