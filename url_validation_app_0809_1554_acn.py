# 代码生成时间: 2025-08-09 15:54:46
from django.http import JsonResponse
from django.views import View
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

"""
A Django application component for validating URL links.

This application provides a simple view that accepts a URL as input,
validates its format using Django's built-in URLValidator,
and returns the result of the validation.
"""

class UrlValidationView(View):
    """
    A view that validates the format of a given URL.
    
    It expects a GET request with a 'url' parameter that contains the URL to validate.
    If the URL is valid, it returns a JSON response with a success message.
    If the URL is invalid, it returns a JSON response with an error message.
    """
    def get(self, request):
        # Fetch the URL from the GET request's query parameters
        url_to_validate = request.GET.get('url')
        
        # Initialize the URLValidator instance
        url_validator = URLValidator()
        
        try:
            # Attempt to validate the URL
            url_validator(url_to_validate)
            # If no exception is raised, the URL is valid
            return JsonResponse({'message': 'URL is valid!'})
        except ValidationError as e:
            # If a ValidationError is raised, the URL is invalid
            return JsonResponse({'error': str(e)}, status=400)

# Define the URL patterns for this application
url_patterns = [
    # Map the URL path 'validate-url/' to the UrlValidationView
    path('validate-url/', UrlValidationView.as_view(), name='validate-url'),
]
