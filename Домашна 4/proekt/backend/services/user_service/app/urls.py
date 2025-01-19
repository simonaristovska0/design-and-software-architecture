from django.urls import path
from .views import LoginAPIView, LogoutAPIView, RegisterAPIView
from django.http import JsonResponse

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('', lambda request: JsonResponse({'message': 'Welcome to user_service'})),
]
