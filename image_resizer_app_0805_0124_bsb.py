# 代码生成时间: 2025-08-05 01:24:55
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from PIL import Image
from io import BytesIO
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import os
import logging

"