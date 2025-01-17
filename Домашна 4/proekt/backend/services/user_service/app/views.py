from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import logout
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class LoginAPIView(APIView):
    """
    API endpoint for user login.
    """

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            raise AuthenticationFailed("Invalid username or password")

        # Return success response
        return Response({"message": "Login successful", "username": user.username})


class LogoutAPIView(APIView):
    """
    API endpoint for user logout.
    """

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"})


class RegisterAPIView(APIView):
    """
    API endpoint for user registration.
    """

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        # Validate if the user already exists
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return Response({"message": "User registered successfully"})
