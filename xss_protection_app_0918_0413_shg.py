# 代码生成时间: 2025-09-18 04:13:25
from django import forms
from django.http import HttpResponse
from django.utils.html import escape
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

"""
Django application component for XSS (Cross-Site Scripting) protection.

This application provides a simple model for storing user input, a view to handle user input and
render a template with proper escaping to prevent XSS attacks.
"""

class SafeInputForm(forms.Form):
    """
    Form for accepting user input with XSS protection.
    
    Uses Django's built-in escaping to prevent XSS attacks.
    """
    user_input = forms.CharField(label='Enter your text', max_length=200)

    def clean_user_input(self):
        """
        Clean the user input by escaping any HTML tags to prevent XSS.
        """
        cleaned_input = escape(self.cleaned_data.get('user_input', ''))
        return cleaned_input

@csrf_exempt
@require_http_methods(['POST'])
def safe_input_view(request):
    """
    View function to handle user input and prevent XSS.
    
    If the form is valid, it escapes the user input to prevent XSS attacks and
    renders a template with the escaped input.
    """
    form = SafeInputForm(request.POST)
    if form.is_valid():
        escaped_input = form.cleaned_data['user_input']
        return HttpResponse(f"User input: {escaped_input}")
    else:
        return HttpResponse("Invalid input.", status=400)

# Define URLs for the application if needed
# from django.urls import path
# urlpatterns = [
#     path('safe-input/', safe_input_view, name='safe_input'),
# ]