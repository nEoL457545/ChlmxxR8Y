# 代码生成时间: 2025-09-08 22:41:36
from django.db import models
from django.urls import path
from django.http import HttpResponse, Http404
from django.views import View
from django.shortcuts import render

"""
This Django application component is designed to create a blog application.
It includes data model design, views, and URLs following Django best practices.
"""

# Data model design
class Post(models.Model):
    """
    A model representing a blog post.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Views
class PostListView(View):
    """
    A view to display a list of all blog posts.
    """
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'blog/post_list.html', {'posts': posts})

class PostDetailView(View):
    """
    A view to display a single blog post.
    """
    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            return render(request, 'blog/post_detail.html', {'post': post})
        except Post.DoesNotExist:
            raise Http404("Post does not exist")

# URLs
app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]
