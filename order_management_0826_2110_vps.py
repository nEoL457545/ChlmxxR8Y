# 代码生成时间: 2025-08-26 21:10:29
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

# Models
class Product(models.Model):
    """Model representing a product."""
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

class Order(models.Model):
    """Model representing an order."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} for {self.product.name}"

# Views
class OrderCreateView(View):
    """Create a new order."""
    def post(self, request, *args, **kwargs):
        """Handle POST request to create an order."""
        try:
            product_id = request.POST.get('product_id')
            quantity = int(request.POST.get('quantity'))
            product = Product.objects.get(id=product_id)
            Order.objects.create(product=product, quantity=quantity)
            return JsonResponse({'message': 'Order created successfully.'}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Product not found.'}, status=404)
        except ValueError:
            return JsonResponse({'error': 'Invalid quantity.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class OrderListView(View):
    """List all orders."""
    def get(self, request, *args, **kwargs):
        """Handle GET request to list all orders."""
        orders = Order.objects.all()
        order_list = [{'id': order.id, 'product_name': order.product.name, 'quantity': order.quantity} for order in orders]
        return JsonResponse(order_list, safe=False)

# URL Patterns
urlpatterns = [
    path('create/', csrf_exempt(OrderCreateView.as_view()), name='create_order'),
    path('list/', csrf_exempt(OrderListView.as_view()), name='list_orders'),
]