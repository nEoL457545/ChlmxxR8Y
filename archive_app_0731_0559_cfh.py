# 代码生成时间: 2025-07-31 05:59:22
from django.conf.urls import url
from django.shortcuts import render
from django.views import View
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
import os
import zipfile
import tarfile
import shutil
from io import BytesIO

"""
Archive App: A Django application to handle file extraction.
This app includes models, views, and URLs to compress and extract
files in various formats.
"""

class ArchiveModel(models.Model):
    """Model to store information about the archived files."""
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    extraction_path = models.CharField(max_length=255)
    def __str__(self):
        return self.file_name

class ExtractArchiveView(View):
    """View to handle extracting archives."""
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        """Extracts the uploaded file."""
        try:
            file = request.FILES.get('file')
            if file is None:
                raise ValueError('No file uploaded.')
            file_name = file.name
            file_path = os.path.join('uploads', file_name)

            # Store the uploaded file
            with default_storage.open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Extract the file
            extraction_path = os.path.join('extracted', file_name.split('.')[0])
            with open(file_path, 'rb') as uploaded_file:
                content = uploaded_file.read()
                
                # Determine file type and extract accordingly
                if file_name.endswith('.zip'):
                    with zipfile.ZipFile(BytesIO(content)) as zip_file:
                        zip_file.extractall(extraction_path)
                elif file_name.endswith(('.tar.gz', '.tgz')):
                    with tarfile.TarFile(fileobj=BytesIO(content), mode='r:gz') as tar_file:
                        tar_file.extractall(extraction_path)
                else:
                    raise ValueError('Unsupported file format.')

            # Save the archive model
            archive = ArchiveModel.objects.create(
                file_name=file_name,
                file_path=file_path,
                extraction_path=extraction_path
            )
            messages.success(request, 'File extracted successfully.')
            return HttpResponseRedirect('success_page')
        except Exception as e:
            messages.error(request, str(e))
            return HttpResponseRedirect('error_page')

archive_app_patterns = [
    path('extract/', ExtractArchiveView.as_view(), name='extract_archive'),
]

urlpatterns = [
    path('archive/', include(archive_app_patterns)),
]
