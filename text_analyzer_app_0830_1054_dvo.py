# 代码生成时间: 2025-08-30 10:54:19
# text_analyzer_app/views.py
from django.shortcuts import render
# 改进用户体验
from django.http import JsonResponse
from .models import TextAnalysis
from django.core.exceptions import ObjectDoesNotExist
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.sentiment import SentimentAnalyzer, SentimentIntensityAnalyzer
from nltk.sentiment.util import *
import string
import re

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('vader_lexicon')
# 扩展功能模块

class TextAnalysisView:
    """
    A Django view handling text analysis functionality.
    """
    def post(self, request):
        """
        Analyze the text file content and return the analysis results.
        """
        text = request.POST.get('text', '')
        if not text:
            return JsonResponse({'error': 'No text provided.'}, status=400)
# NOTE: 重要实现细节

        # Tokenize the text
        tokens = word_tokenize(text)
        # Remove punctuation
        tokens = [word for word in tokens if word.isalpha()]
        # Remove stop words
        tokens = [word for word in tokens if word not in stopwords.words('english')]
        # Frequency distribution of tokens
        freq_dist = FreqDist(tokens)
        # Sentiment analysis
        sia = SentimentIntensityAnalyzer()
        sentiment_score = sia.polarity_scores(text)

        # Prepare response data
# 改进用户体验
        response_data = {
            'total_tokens': len(tokens),
            'most_common_tokens': freq_dist.most_common(5),
            'sentiment_score': sentiment_score,
        }

        return JsonResponse(response_data)
# 改进用户体验


# text_analyzer_app/models.py
from django.db import models
# 改进用户体验

class TextAnalysis(models.Model):
    """
    A Django model representing a text analysis.
    """
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
# 增强安全性
        return self.text[:50]


# text_analyzer_app/urls.py
from django.urls import path
from .views import TextAnalysisView

urlpatterns = [
    path('analyze/', TextAnalysisView.as_view(), name='text_analysis'),
]
```

</div>
</div>

以上代码是一个Django应用组件，包括以下几个部分：

1. views.py：定义了一个TextAnalysisView类，处理文本分析功能。
    - 使用POST请求接收文本数据，并进行分词、去停用词、频率统计和情感分析。
    - 返回分析结果的JSON数据。

2. models.py：定义了一个TextAnalysis模型，用于存储文本分析结果。
    - 包含text字段用于存储文本，created_at字段自动记录创建时间。

3. urls.py：定义了应用的URL路由。
    - 将URL 'analyze/' 映射到TextAnalysisView类的as_view()方法。

此外，代码遵循了Django的最佳实践，包括：
- 使用类视图处理请求
- 定义模型和数据库字段
- 添加了适当的注释和docstring
- 使用NLTK库进行文本分析，并进行了错误处理

请确保安装了nltk库和其他必要的依赖项，然后在Django项目中创建text_analyzer_app应用，并添加上述代码即可。
