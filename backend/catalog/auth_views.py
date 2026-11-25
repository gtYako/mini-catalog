from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@ensure_csrf_cookie
@api_view(['GET'])
@permission_classes([AllowAny])
def session_info(request):
    return Response({'is_staff': bool(request.user.is_authenticated and request.user.is_staff)})

@csrf_protect
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login_view(request):
    user = authenticate(request, username=request.data.get('username'), password=request.data.get('password'))
    if user is None or not user.is_staff:
        return Response({'detail': 'Неверный логин или пароль администратора.'}, status=403)
    login(request, user)
    return Response({'is_staff': True})

@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    logout(request)
    return Response({'is_staff': False})
