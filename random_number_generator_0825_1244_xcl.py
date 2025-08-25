# 代码生成时间: 2025-08-25 12:44:37
import random
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views import View
from django.http import Http404
from django.utils.decorators import method_decorator
def generate_random_number(min_value, max_value):
    """
    Generates a random number between min_value and max_value.
    :param min_value: The minimum possible value for the generated number.
    :param max_value: The maximum possible value for the generated number.
    :return: A random integer between min_value and max_value (inclusive).
    """
    return random.randint(min_value, max_value)

class RandomNumberGeneratorView(View):
    """
    A Django view that generates a random number when requested.
    """
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to the /random-number/ endpoint.
        :return: A JSON response with the generated random number.
        """
        try:
            min_value = request.GET.get('min', 0)
            max_value = request.GET.get('max', 100)
            # Ensure min and max are integers
            min_value = int(min_value)
            max_value = int(max_value)
        except ValueError:
            # Handle the case where the values are not integers
            return JsonResponse({'error': 'Invalid input, min and max must be integers.'}, status=400)
        except ObjectDoesNotExist:
            # If the parameters are not provided, default values are used
            min_value = 0
            max_value = 100
        
        # Check if min_value is less than max_value
        if min_value >= max_value:
            return JsonResponse({'error': 'min must be less than max.'}, status=400)
        
        # Generate the random number
        random_number = generate_random_number(min_value, max_value)
        return JsonResponse({'random_number': random_number})
    
# Example of a Django URL configuration
#from django.urls import path
#from .views import RandomNumberGeneratorView
#
#urlpatterns = [
#    path('random-number/', RandomNumberGeneratorView.as_view(), name='random_number'),
#]
