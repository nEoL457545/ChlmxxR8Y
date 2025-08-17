# 代码生成时间: 2025-08-17 17:15:46
# Django application for user login verification

"""
Contains the models, views, and URLs for a basic user login system in Django.
This module follows Django best practices and includes error handling.
"""

from django.db import models
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator

import json
import logging

# Setup logging
logger = logging.getLogger(__name__)

class UserModel(models.Model):
    """
    Custom user model extending Django's base User model.
    If you need additional fields on users, extend this model.
    """
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        help_text='Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only.'
    )
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

class LoginView:
    """
    View to handle user login requests.
    """
    @require_http_methods(['POST'])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        """
        Handles the POST request for user login.
        Validates the request and authenticates the user.
        """
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({'error': 'Missing username or password'}, status=400)

            user = User.objects.get(username=username)
            if authenticate(username=username, password=password):
                login(request, user)
                return JsonResponse({'message': 'User logged in successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid username or password'}, status=401)

        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            logger.error(f'An error occurred: {e}')
            return JsonResponse({'error': 'Internal server error'}, status=500)

# URL patterns for the login app
urlpatterns = [
    # Define the URL pattern for the login view
    path('login/', LoginView.as_view(), name='login'),
]

# Note: This example assumes you have a Django project set up and this app is included in your INSTALLED_APPS and urls.py.

# You might need to adjust this code to fit into your existing project structure.
