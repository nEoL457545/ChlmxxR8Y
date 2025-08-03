# 代码生成时间: 2025-08-03 17:56:53
from django.contrib.auth.models import User, auth
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import path
from django.conf import settings
from django.contrib.auth.decorators import login_required
import json

# Models
# Assuming we have a basic User model which is provided by Django

# Views
@csrf_exempt
@require_http_methods(['POST'])
def user_login(request):
    """
    Handle user login.
    
    Request parameters:
    - username (str): The username of the user.
    - password (str): The password of the user.
    
    Response:
    - A JSON object containing the login status and user information.
    """
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return JsonResponse({'error': 'Username and password are required.'}, status=400)
    
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return JsonResponse({'message': 'Login successful.', 'user': user.id})
    else:
        return JsonResponse({'error': 'Invalid credentials.'}, status=401)

@csrf_exempt
@require_http_methods(['POST'])
def user_logout(request):
    """
    Handle user logout.
    
    Response:
    - A JSON object indicating logout status.
    """
    logout(request)
    return JsonResponse({'message': 'Logout successful.'})

@csrf_exempt
@require_http_methods(['POST'])
def user_register(request):
    """
    Register a new user.
    
    Request parameters:
    - username (str): The username of the user.
    - password (str): The password of the user.
    - email (str): The email address of the user.
    
    Response:
    - A JSON object indicating registration status and user information.
    """
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if not username or not password or not email:
        return JsonResponse({'error': 'Username, password, and email are required.'}, status=400)
    
    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return JsonResponse({'message': 'Registration successful.', 'user': user.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# URLs
urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
]
