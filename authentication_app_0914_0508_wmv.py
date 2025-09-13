# 代码生成时间: 2025-09-14 05:08:41
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError


class AuthView(View):
    """
    用户身份认证视图，提供登录和登出功能。
    """

    def post(self, request):
        """
        处理用户登录请求。
        """
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return JsonResponse({'error': '用户名和密码都必须提供。'}, status=400)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': '登录成功。'}, status=200)
        else:
            return JsonResponse({'error': '用户名或密码错误。'}, status=401)

    def delete(self, request):
        """
        处理用户登出请求。
        """
        logout(request)
        return JsonResponse({'message': '登出成功。'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class RegistrationView(View):
    """
    用户注册视图，接收用户注册请求。
    """
    def post(self, request):
        """
        处理用户注册请求。
        """
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if not username or not password or not email:
            return JsonResponse({'error': '用户名、密码和邮箱都必须提供。'}, status=400)

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            login(request, user)
            return JsonResponse({'message': '注册并登录成功。'}, status=201)
        except ValidationError as e:
            return JsonResponse({'error': e.message_dict}, status=400)


# urls.py
from django.urls import path
from .views import AuthView, RegistrationView

urlpatterns = [
ed
    path('auth/login/', AuthView.as_view(), name='auth_login'),
    path('auth/logout/', AuthView.as_view(), name='auth_logout'),
    path('auth/register/', RegistrationView.as_view(), name='auth_register'),
]
