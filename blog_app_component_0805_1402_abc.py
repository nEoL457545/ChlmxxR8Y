# 代码生成时间: 2025-08-05 14:02:35
from django.db import models
from django.urls import path
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict

# Models
class Blog(models.Model):
    """Blog model with title and content."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    def __str__(self):
        return self.title

# Views
@method_decorator(csrf_exempt, name='dispatch')
class BlogView(View):
    """View for handling blog operations."""
    
    def get(self, request):
        """Handle GET request and return a list of blogs."""
        blogs = Blog.objects.all()
        return JsonResponse(list(model_to_dict(blog) for blog in blogs), safe=False)
    
    def post(self, request):
        """Handle POST request to create a new blog."""
        try:
            data = request.POST.dict()
            blog = Blog(title=data['title'], content=data['content'])
            blog.save()
            return JsonResponse(model_to_dict(blog), status=201)
        except KeyError:
            return JsonResponse({'error': 'Missing title or content'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def put(self, request, blog_id):
        """Handle PUT request to update a blog."""
        try:
            blog = Blog.objects.get(id=blog_id)
            data = request.POST.dict()
            blog.title = data.get('title', blog.title)
            blog.content = data.get('content', blog.content)
            blog.save()
            return JsonResponse(model_to_dict(blog))
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Blog not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def delete(self, request, blog_id):
        """Handle DELETE request to delete a blog."""
        try:
            blog = Blog.objects.get(id=blog_id)
            blog.delete()
            return JsonResponse({'message': 'Blog deleted successfully'}, status=204)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Blog not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# URL Patterns
urlpatterns = [
    path('blogs/', BlogView.as_view(), name='blogs'),
    path('blogs/<int:blog_id>/', BlogView.as_view(), name='blog_detail'),
]
