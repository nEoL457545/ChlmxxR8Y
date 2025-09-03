# 代码生成时间: 2025-09-04 07:28:47
# notification_app
# A Django application component for a message notification system.

"""
notification_app
==============

This Django app provides a simple message notification system.
It includes models, views, and URLs following Django best practices.
"""

# models.py
from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    """Model for storing notifications."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')  # 关联用户
    message = models.TextField()  # 消息文本
    is_read = models.BooleanField(default=False)  # 是否已读
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}"

# views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Notification
from django.contrib.auth.decorators import login_required

class NotificationView(View):
    """View for handling notification operations."""
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request, *args, **kwargs):
        """Create a new notification."""
        user_id = request.POST.get('user_id')
        message = request.POST.get('message')
        user = get_object_or_404(User, id=user_id)
        notification = Notification.objects.create(user=user, message=message)
        return JsonResponse({'status': 'success', 'id': notification.id})

    @login_required
    def get(self, request, *args, **kwargs):
        """Retrieve notifications for the current user."""
        notifications = request.user.notifications.all()
        return JsonResponse([{'id': n.id, 'message': n.message, 'is_read': n.is_read, 'created_at': n.created_at.isoformat()} for n in notifications], safe=False)

# urls.py
from django.urls import path
from .views import NotificationView

urlpatterns = [
    path('notification/', NotificationView.as_view(), name='notification'),
]
