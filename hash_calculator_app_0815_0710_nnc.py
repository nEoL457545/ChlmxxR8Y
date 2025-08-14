# 代码生成时间: 2025-08-15 07:10:09
from django.conf import settings
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
import hashlib
import hmac

"""
A Django application component for calculating hash values.
"""

class HashValue(models.Model):
    """
    A model to store hash values.
    """
    original_data = models.TextField(help_text="The original data to be hashed.")
# 增强安全性
    hash_type = models.CharField(max_length=50, help_text="The type of hash to be calculated.")
    hash_value = models.CharField(max_length=128, help_text="The calculated hash value.")
# NOTE: 重要实现细节

    def save(self, *args, **kwargs):
        """
        Calculate the hash value before saving to the database.
        """
        self.hash_value = self.calculate_hash()
# 增强安全性
        super().save(*args, **kwargs)

    def calculate_hash(self):
# 添加错误处理
        """
        Calculate the hash value based on the hash type.
        """
        if self.hash_type == "md5":
            return hashlib.md5(self.original_data.encode()).hexdigest()
        elif self.hash_type == "sha1":
            return hashlib.sha1(self.original_data.encode()).hexdigest()
        elif self.hash_type == "sha256":
            return hashlib.sha256(self.original_data.encode()).hexdigest()
        else:
            raise ValueError("Unsupported hash type.")
# NOTE: 重要实现细节

class HashCalculatorView(View):
    """
    A view to handle hash calculation requests.
# 改进用户体验
    """
    def post(self, request):
        """
        Calculate the hash value based on the provided data and hash type.
        """
        data = request.POST.get('data')
        hash_type = request.POST.get('hash_type')
        
        try:
            hash_value = HashValue.objects.create(
                original_data=data,
                hash_type=hash_type
            ).hash_value
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        return JsonResponse({'hash_value': hash_value})


def hash_calculator_urls():
# 优化算法效率
    """
# 添加错误处理
    Define the URL patterns for the hash calculator application.
    """
    return [
        path('calculate/', HashCalculatorView.as_view(), name='hash_calculator'),
    ]

# Example usage of including the hash_calculator_app in the project's urls.py
# 优化算法效率
# from django.urls import include, path
# from . import hash_calculator_app as hash_calculator_app_module
# urlpatterns = [
#     path('hash_calculator/', include(hash_calculator_app_module.hash_calculator_urls())),
# ]