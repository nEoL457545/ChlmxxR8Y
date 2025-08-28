# 代码生成时间: 2025-08-29 07:10:52
from django.db import models
from django.shortcuts import render
from django.http import JsonResponse
import psutil
import os
import sys

# Define the Model for storing memory usage data
class MemoryUsage(models.Model):
    """Model to store memory usage data."""
    # Timestamp of when the memory usage was recorded
    timestamp = models.DateTimeField(auto_now_add=True)
    # Total physical memory (RAM)
    total_memory = models.BigIntegerField()
    # Available physical memory (RAM)
    available_memory = models.BigIntegerField()
    # Used memory
    used_memory = models.BigIntegerField()
    # Free memory
    free_memory = models.BigIntegerField()
    # Memory usage percentage
    memory_usage_percent = models.FloatField()

    def __str__(self):
        return f"Memory usage on {self.timestamp}"

# Views
def index(request):
    """
    Home page of the memory usage analysis app.
    Displays the latest memory usage data.
    """
    # Get the latest memory usage data
    latest_usage = MemoryUsage.objects.latest('timestamp')
    # Prepare data to be sent to the template
    context = {
        'total_memory': latest_usage.total_memory,
        'available_memory': latest_usage.available_memory,
        'used_memory': latest_usage.used_memory,
        'free_memory': latest_usage.free_memory,
        'memory_usage_percent': latest_usage.memory_usage_percent,
    }
    return render(request, 'memory_usage_analysis/index.html', context)

def get_memory_usage(request):
    """
    API endpoint to get current memory usage data.
    Returns a JSON response with memory usage data.
    """
    try:
        mem = psutil.virtual_memory()
        new_usage = MemoryUsage.objects.create(
            total_memory=mem.total,
            available_memory=mem.available,
            used_memory=mem.used,
            free_memory=mem.free,
            memory_usage_percent=mem.percent,
        )
        return JsonResponse({
            'total_memory': new_usage.total_memory,
            'available_memory': new_usage.available_memory,
            'used_memory': new_usage.used_memory,
            'free_memory': new_usage.free_memory,
            'memory_usage_percent': new_usage.memory_usage_percent,
        })
    except Exception as e:
        # Error handling
        return JsonResponse({'error': str(e)}, status=500)

# URL patterns
from django.urls import path

urlpatterns = [
    path('memory_usage/', get_memory_usage, name='get_memory_usage'),
    path('', index, name='index'),
]
