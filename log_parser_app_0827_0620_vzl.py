# 代码生成时间: 2025-08-27 06:20:58
# Django app for log file parsing

"""
This Django application provides a log file parsing tool.
It allows users to upload log files and retrieve parsed log data.
"""

# models.py
"""
Define models for log file data.
"""
from django.db import models

class LogFile(models.Model):
    """Model to store uploaded log files."""
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='log_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

# views.py
"""
Define views for log file parsing.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import LogFile
from .parser import parse_log_file

@csrf_exempt
@require_http_methods(['POST'])
def upload_log_file(request):
    """
    View to handle log file uploads.
    """
    if request.method == 'POST':
        file = request.FILES.get('log_file')
        if not file:
            return JsonResponse({'error': 'No file provided'}, status=400)
        
        log_file = LogFile.objects.create(name=file.name, file=file)
        parsed_data = parse_log_file(log_file.file)
        return JsonResponse({'data': parsed_data}, status=201)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)

# urls.py
"""
Define URL patterns for the log parser app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_log_file, name='upload_log_file'),
]

# parser.py
"""
Define functions for parsing log files.
"""
import re

def parse_log_file(file_path):
    """
    Parse a log file and return the parsed data.
    """
    log_pattern = re.compile(r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (?P<level>[A-Z]+) - (?P<message>.*)')
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            parsed_data = []
            for line in lines:
                match = log_pattern.match(line)
                if match:
                    parsed_data.append(match.groupdict())
            return parsed_data
    except FileNotFoundError:
        raise ValueError('File not found')
    except Exception as e:
        raise ValueError(f'Error parsing file: {str(e)}')
