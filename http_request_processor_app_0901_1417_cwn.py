# 代码生成时间: 2025-09-01 14:17:02
# django_http_request_processor/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('process/', views.http_request_processor, name='http_request_processor'),
]

# django_http_request_processor/views.py
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from .models import HttpRequestLog
from django.db import IntegrityError

@require_http_methods(['GET', 'POST'])
def http_request_processor(request):
    """
    HTTP request processor view.
    
    This view handles both GET and POST requests, logging each request to the database
    and then responding with a JSON object indicating the nature of the request.
    """
    try:
        # Log the incoming HTTP request.
        request_type = request.method
        HttpRequestLog.objects.create(
            request_type=request_type,
            url=request.path,
            query_params=request.GET.urlencode(),
            raw_post_data=request.body,
        )
    except IntegrityError:
        return HttpResponse("Error processing request.", status=500)
    
    # Prepare response data.
    response_data = {
        "status": "success",
        "method": request.method,
        "path": request.path,
        "query_params": request.GET.urlencode(),
        "raw_post_data": request.POST.urlencode() if request.method == 'POST' else '',
    }
    return JsonResponse(response_data)

# django_http_request_processor/models.py
from django.db import models

class HttpRequestLog(models.Model):
    """
    Model for logging HTTP requests.
    
    Attributes:
    - request_type (str): The type of the HTTP request (e.g., GET, POST).
    - url (str): The URL of the request.
    - query_params (str): The URL-encoded query parameters.
    - raw_post_data (str): The raw post data for POST requests.
    """
    request_type = models.CharField(max_length=10)
    url = models.CharField(max_length=200)
    query_params = models.TextField()
    raw_post_data = models.TextField()
    
    def __str__(self):
        return f"HttpRequestLog: {self.request_type} {self.url}"