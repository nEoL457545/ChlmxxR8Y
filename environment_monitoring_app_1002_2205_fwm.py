# 代码生成时间: 2025-10-02 22:05:42
from django.db import models
from django.views import View
from django.http import JsonResponse
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from datetime import datetime
import logging

# 设置日志记录
logger = logging.getLogger(__name__)


# Models
class EnvironmentData(models.Model):
    """存储环境监测数据的模型"""
    temperature = models.FloatField(verbose_name="Temperature in Celsius")
    humidity = models.FloatField(verbose_name="Humidity Percentage")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp of measurement")

    def __str__(self):
        """返回环境数据的字符串表示"""
        return f"{self.temperature}°C, {self.humidity}% at {self.timestamp}"


# Views
class EnvironmentDataView(View):
    """视图来处理环境监测数据的CRUD操作"""
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request, *args, **kwargs):
        """创建新的环境监测数据条目"""
        try:
            data = request.POST
            temperature = float(data.get('temperature', 0))
            humidity = float(data.get('humidity', 0))
            EnvironmentData.objects.create(temperature=temperature, humidity=humidity)
            return JsonResponse({'message': 'Data created successfully'}, status=201)
        except ValidationError as e:
            logger.error(f'Validation error: {e}')
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            logger.error(f'Unexpected error: {e}')
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

    def get(self, request, *args, **kwargs):
        """获取所有的环境监测数据条目"""
        try:
            data_list = EnvironmentData.objects.all()
            return JsonResponse(list(data_list.values()), safe=False)
        except Exception as e:
            logger.error(f'Unexpected error: {e}')
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)


# URLs
urlpatterns = [
    path('data/', EnvironmentDataView.as_view(), name='environment_data'),
]
