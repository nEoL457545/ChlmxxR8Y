# 代码生成时间: 2025-08-31 02:52:41
from django.db import models
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.urls import path


# Models
class Product(models.Model):  # Product model to store product details
    """Model representing a product in the catalog."""
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):  # String representation of the Product
        return self.name


# Views
@require_http_methods(["GET", "POST"])
def add_to_cart(request, product_id):  # Function to add a product to the cart
    """Adds a product to the shopping cart."""
    try:  # Attempt to retrieve the product
        product = Product.objects.get(id=product_id)
    except ObjectDoesNotExist:  # Handle the case where product does not exist
        return JsonResponse({'error': 'Product not found'}, status=404)

    if request.method == 'POST':  # If the request is a POST, add product to the cart
        from django.contrib.sessions.models import Session
        session = request.session  # Retrieve session object for cart
        cart = session.get('cart', {})  # Retrieve the cart from session or create a new one
        cart[product_id] = cart.get(product_id, 0) + 1  # Increment the product quantity or add it
        session['cart'] = cart  # Update the session with the new cart
        return JsonResponse({'success': 'Product added to cart', 'cart': cart}, status=200)
    else:  # If the request is a GET, show the product details
        return render(request, 'product_detail.html', {'product': product})


# URLs
urlpatterns = [  # Define URL patterns for the application
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add-to-cart'),  # URL pattern for adding a product to the cart
]
