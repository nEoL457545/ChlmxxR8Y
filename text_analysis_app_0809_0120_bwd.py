# 代码生成时间: 2025-08-09 01:20:54
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import TextAnalysis
# 优化算法效率
import os
import numpy as np
import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

# 确保NLTK数据包已下载
nltk.download('punkt')
nltk.download('stopwords')

# Spacy模型加载
nlp = spacy.load('en_core_web_sm')

# 创建模型文件
class TextAnalysis(models.Model):
    file = models.FileField(upload_to='uploads/')
    
    def __str__(self):
        """返回模型的字符串表示形式"""
        return self.file.name
    
    # 提供文本分析方法
    def analyze_text(self):
        """
        分析上传文件中的文本，并返回分析结果。
# 改进用户体验
        
        返回值:
        A dictionary containing text analysis results.
        """
        try:
            with self.file.open('r') as file:
                content = file.read()
            
            # 词性标注
            doc = nlp(content)
# 增强安全性
            pos_tags = [(token.text, token.pos_) for token in doc]
            
            # 词频统计
# NOTE: 重要实现细节
            words = word_tokenize(content)
            word_freq = Counter(words)
            
            # 去除停用词
            stop_words = set(stopwords.words('english'))
# 改进用户体验
            filtered_words = [word for word in words if word.lower() not in stop_words]
            filtered_word_freq = Counter(filtered_words)
            
            # 返回分析结果
# TODO: 优化性能
            return {
                'pos_tags': pos_tags,
                'word_freq': dict(word_freq),
                'filtered_word_freq': dict(filtered_word_freq)
            }
        except Exception as e:
# 优化算法效率
            return {'error': str(e)}

# 创建视图
@require_http_methods(['POST'])
def text_analysis_view(request):
    """
    处理文件上传并分析文本。
    
    参数:
    request - HTTP请求对象。
    
    返回值:
    JsonResponse - 包含文本分析结果的JSON响应。
    """
    try:
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'error': 'No file provided.'}, status=400)
        
        # 保存上传的文件
        text_analysis = TextAnalysis.objects.create(file=file)
        
        # 分析文本
# 扩展功能模块
        analysis_results = text_analysis.analyze_text()
# 增强安全性
        return JsonResponse(analysis_results)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# URL配置
urlpatterns = [
    path('analyze/', text_analysis_view, name='text_analysis'),
]
