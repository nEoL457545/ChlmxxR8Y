# 代码生成时间: 2025-10-08 19:52:48
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods


# Models
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    """Model representing an Order with properties such as product name, quantity, and status."""
    def __str__(self):
        return self.product_name


# Views
class OrderCreateView(View):
    """View to create a new order."""
    @require_http_methods(['POST'])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        try:
            product_name = request.POST.get('product_name')
            quantity = int(request.POST.get('quantity', 1))
            order = Order.objects.create(product_name=product_name, quantity=quantity)
            return JsonResponse({'message': 'Order created successfully.', 'order_id': order.id})
        except ValueError as e:
            return JsonResponse({'error': 'Invalid input data.'}, status=400)


class OrderUpdateView(View):
    """View to update the status of an order."""
    @require_http_methods(['PUT'])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def put(self, request, pk):
        try:
            order = get_object_or_404(Order, pk=pk)
            status = request.PUT.get('status')
            if status in Order.STATUS_CHOICES:
                order.status = status
                order.save()
                return JsonResponse({'message': 'Order updated successfully.', 'status': order.status})
            else:
                return JsonResponse({'error': 'Invalid status.'}, status=400)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found.'}, status=404)
        except ValueError as e:
            return JsonResponse({'error': 'Invalid input data.'}, status=400)


# URLs
urlpatterns = [
    path('order/', OrderCreateView.as_view(), name='order-create'),
    path('order/<int:pk>/', OrderUpdateView.as_view(), name='order-update'),
]
