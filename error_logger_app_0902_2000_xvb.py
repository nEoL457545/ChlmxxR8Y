# 代码生成时间: 2025-09-02 20:00:49
# error_logger/models.py
"""
This module contains the model for the ErrorLog.
"""
from django.db import models
import logging

class ErrorLog(models.Model):
    """Model representing an error log."""
    message = models.TextField(help_text="The error message.")
    traceback = models.TextField(blank=True, help_text="The traceback of the error.")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="The time the error was logged.")
    level = models.CharField(max_length=10, choices=[
        ('debug', 'Debug'),
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('critical', 'Critical')], default='error',
        help_text="The level of the error.")
    logger_name = models.CharField(max_length=255, help_text="The name of the logger.")
    
    def __str__(self):
        return f"{self.logger_name} - {self.get_level_display()}"

# error_logger/views.py
"""
This module contains the view for the error log.
"""
from django.shortcuts import render
from .models import ErrorLog
from django.views.generic import ListView

class ErrorLogListView(ListView):
    """
    View to display a list of error logs.
    """
    model = ErrorLog
    template_name = 'error_logger/error_log_list.html'
    context_object_name = 'error_logs'
    
    def get_queryset(self):
        return ErrorLog.objects.all().order_by('-timestamp')

# error_logger/urls.py
"""
This module contains the URL patterns for the error logger view.
"""
from django.urls import path
from .views import ErrorLogListView

urlpatterns = [
    path('error-logs/', ErrorLogListView.as_view(), name='error-log-list'),
]

# error_logger/consumer.py
"""
This module contains a WebSocket consumer to handle error logging.
"""
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import ErrorLog
import logging

class ErrorLogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
    
    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        traceback = text_data_json.get('traceback', "")
        level = text_data_json.get('level', 'error')
        logger_name = text_data_json.get('logger_name', 'default')
        await self.send(text_data=json.dumps(
            {'message': f"Error logged successfully."}
        ))
        logging.log(getattr(logging, level.upper()), message)
        ErrorLog.objects.create(
            message=message,
            traceback=traceback,
            level=level,
            logger_name=logger_name
        )

# error_logger/admin.py
"""
This module contains the admin interface for the ErrorLog model.
"""
from django.contrib import admin
from .models import ErrorLog

admin.site.register(ErrorLog)
