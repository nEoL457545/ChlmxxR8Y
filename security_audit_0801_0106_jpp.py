# 代码生成时间: 2025-08-01 01:06:00
from django.db import models
from django.utils import timezone
from django.urls import path
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

# 定义安全审计日志 Model
class SecurityAuditLog(models.Model):
    # 用户ID
    user_id = models.IntegerField()
    # 操作类型
    operation_type = models.CharField(max_length=255)
    # 操作描述
    operation_description = models.TextField()
    # 操作时间
    operation_time = models.DateTimeField(default=timezone.now)
    # 用户IP地址
    user_ip = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user_id} - {self.operation_type} - {self.operation_time}"

# 定义视图
class SecurityAuditView(View):
    def post(self, request):
        # 获取请求数据
        data = json.loads(request.body)
        user_id = data.get('user_id')
        operation_type = data.get('operation_type')
        operation_description = data.get('operation_description')
        user_ip = request.META.get('REMOTE_ADDR')

        # 校验数据
        if not all([user_id, operation_type, operation_description, user_ip]):
            return HttpResponse(json.dumps({'error': 'Missing required fields'}), status=400, content_type='application/json')

        # 创建安全审计日志
        SecurityAuditLog.objects.create(
            user_id=user_id,
            operation_type=operation_type,
            operation_description=operation_description,
            user_ip=user_ip
        )

        # 返回成功响应
        return HttpResponse(json.dumps({'message': 'Security audit log created successfully'}), status=201, content_type='application/json')

# URL配置
audit_log_url = path('audit_log/', SecurityAuditView.as_view(), name='audit_log')

# 导出URL配置，以供其他模块使用
urlpatterns = [
    audit_log_url
]
