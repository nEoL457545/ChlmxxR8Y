# 代码生成时间: 2025-09-15 10:05:30
from django.db import models
def __init__(self, **kwargs):
    # 初始化方法
    super().__init__(**kwargs)

    class Post(models.Model):
        # 文章模型"""
        title = models.CharField(max_length=200, help_text="文章标题")
        content = models.TextField(help_text="文章内容")
        author = models.ForeignKey("auth.User", on_delete=models.CASCADE, help_text="文章作者")
        created_at = models.DateTimeField(auto_now_add=True, help_text="文章创建时间")
        updated_at = models.DateTimeField(auto_now=True, help_text="文章更新时间")
        
        class Meta:
            # 元数据配置，用于排序
            ordering = ["-created_at"]
        
        def __str__(self):
            # 返回对象的字符串表示
            return self.title"""
        
        class Comment(models.Model):
            # 评论模型"""
            post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", help_text="评论所属文章")
            author = models.ForeignKey("auth.User", on_delete=models.CASCADE, help_text="评论作者")
            content = models.TextField(help_text="评论内容")
            created_at = models.DateTimeField(auto_now_add=True, help_text="评论创建时间")
            
            class Meta:
                # 元数据配置，用于排序
                ordering = ["-created_at"]
            
            def __str__(self):
                # 返回对象的字符串表示
                return f"Comment by {self.author} on {self.post}"

    
    from django.shortcuts import render, get_object_or_404
def post_list(request):
    # 文章列表视图"""
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})
    
    def post_detail(request, pk):
        # 文章详情视图"""
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post': post})
    
    def post_create(request):
        # 文章创建视图"""
        if request.method == 'POST':
            post = Post.objects.create(
                title=request.POST.get('title'),
                content=request.POST.get('content'),
                author=request.user
            )
            return redirect('post_detail', pk=post.pk)
        return render(request, 'blog/post_edit.html')
    
    def post_update(request, pk):
        # 文章更新视图"""
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST':
            post.title = request.POST.get('title', post.title)
            post.content = request.POST.get('content', post.content)
            post.save()
            return redirect('post_detail', pk=post.pk)
        return render(request, 'blog/post_edit.html', {'post': post})
    
    def post_delete(request, pk):
        # 文章删除视图"""
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST':
            post.delete()
            return redirect('post_list')
        return render(request, 'blog/post_confirm_delete.html', {'post': post})
    
    from django.urls import path
def blog_app_urls():
    # blog应用的URL配置"""
    return [
        path("", post_list, name="post_list"),
        path("post/<int:pk>/", post_detail, name="post_detail"),
        path("post/new/", post_create, name="post_create"),
        path("post/<int:pk>/edit/", post_update, name="post_update"),
        path("post/<int:pk>/delete/", post_delete, name="post_delete"),
        path("post/<int:post_pk>/comment/", post_comment, name="add_comment"),
    ]
    
    def post_comment(request, post_pk):
        # 添加评论视图"""
        post = get_object_or_404(Post, pk=post_pk)
        if request.method == 'POST':
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                content=request.POST.get('content')
            )
            return redirect('post_detail', pk=post_pk)
        return render(request, 'blog/add_comment.html', {'post': post})
