# 代码生成时间: 2025-09-05 06:37:50
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ImproperlyConfigured
import requests
import socket
from urllib.parse import urlparse
"""
网络连接状态检查器组件
"""

class NetworkConnectionChecker(View):
    def get(self, request, *args, **kwargs):
        """
        处理GET请求，检查网络连接状态
        :param request: HttpRequest对象
        :return: JsonResponse对象，包含连接状态结果
        """
        try:
            url = request.GET.get('url')
            if not url:
                return JsonResponse({'error': 'URL 参数未提供'}, status=400)
            # 解析URL
            parsed_url = urlparse(url)
            # 检查协议是否支持
            if parsed_url.scheme not in ['http', 'https']:
                return JsonResponse({'error': '不支持的URL协议'}, status=400)
            # 检查网络连接
            try:
                # 使用requests库发起HEAD请求，检测网络连接
                response = requests.head(url, timeout=5)
                if response.status_code == 200:
                    return JsonResponse({'status': 'connected', 'url': url})
                else:
                    return JsonResponse({'status': 'disconnected', 'url': url, 'error': '服务器返回非200状态码'})
            except requests.ConnectionError:
                return JsonResponse({'status': 'disconnected', 'url': url, 'error': '网络连接错误'})
            except requests.Timeout:
                return JsonResponse({'status': 'disconnected', 'url': url, 'error': '请求超时'})
        except Exception as e:
            # 处理未预料的异常
            return JsonResponse({'error': '服务器错误', 'message': str(e)}, status=500)
