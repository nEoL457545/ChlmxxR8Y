# 代码生成时间: 2025-09-12 14:05:31
from django.db import models
from django.http import JsonResponse
from django.urls import path
from django.views import View
import random
import string


# Define the model for test data
class TestData(models.Model):
    """ Model representing test data. """
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# View to generate test data
class GenerateTestDataView(View):
    """ View to generate and save test data. """
    def get(self, request, *args, **kwargs):
        """ Handles GET request to generate test data. """
        try:
            # Generate test data
            test_data = self.generate_test_data()
            # Save test data to database
            TestData.objects.create(**test_data)
            # Return success message
            return JsonResponse({'message': 'Test data generated successfully.'}, status=200)
        except Exception as e:
            # Return error message if an exception occurs
            return JsonResponse({'error': str(e)}, status=500)

    def generate_test_data(self):
        """ Generates random test data. """
        name = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
        email = f"{random.choice(string.ascii_lowercase + string.digits)}@example.com"
        phone = f"+{random.randint(1, 99)}{random.randint(100000000, 999999999)}"
        return {
            'name': name,
            'email': email,
            'phone': phone,
        }


# Define URL patterns
urlpatterns = [
    path('generate-test-data/', GenerateTestDataView.as_view(), name='generate_test_data'),
]
