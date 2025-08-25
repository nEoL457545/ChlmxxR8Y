# 代码生成时间: 2025-08-25 18:42:08
# bulk_rename_app/models.py
"""
Defines the models for the Bulk Rename Application.
"""
from django.db import models
from django.core.exceptions import ValidationError
import os

class File(models.Model):
    """
    A model representing a file to be renamed.
    """
    old_name = models.CharField(max_length=255, help_text="The current name of the file.")
    new_name = models.CharField(max_length=255, blank=True, help_text="The new name of the file.")

    def clean(self):
        """
        Validate the file model fields.
        """
        if not os.path.exists(self.old_name):
            raise ValidationError(f"The file {self.old_name} does not exist.")

    def save(self, *args, **kwargs):
        """
        Override the save method to perform file renaming.
        """
        self.clean()
        super().save(*args, **kwargs)
        if self.new_name:
            os.rename(self.old_name, self.new_name)

# bulk_rename_app/views.py
"""
Handles the logic for renaming files in bulk.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import File
from django.http import HttpResponse

def bulk_rename(request):
    """
    View to handle file renaming.
    """
    if request.method == 'POST':
        files = request.POST.getlist('file')
        for file_info in files:
            old_name = file_info.get('old_name')
            new_name = file_info.get('new_name')
            try:
                file = File(old_name=old_name, new_name=new_name)
                file.save()
                messages.success(request, f"File {old_name} renamed to {new_name}.")
            except ValidationError as e:
                messages.error(request, str(e))
        return redirect('bulk_rename')
    return render(request, 'bulk_rename.html')

# bulk_rename_app/urls.py
"""
Defines the URL patterns for the Bulk Rename Application.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('bulk_rename/', views.bulk_rename, name='bulk_rename'),
]

# bulk_rename_app/templates/bulk_rename.html
"""
Template for bulk renaming files.
"""
<form method='post'>
    {% csrf_token %}
    <div id='file-list'>
        {% for file in files %}
        <div class='file-item'>
            <label for='old_name_{{ forloop.counter0 }}'>Old Name:</label>
            <input type='text' name='file[{{ forloop.counter0 }}][old_name]' id='old_name_{{ forloop.counter0 }}' value='{{ file.old_name }}'>
            <label for='new_name_{{ forloop.counter0 }}'>New Name:</label>
            <input type='text' name='file[{{ forloop.counter0 }}][new_name]' id='new_name_{{ forloop.counter0 }}' value='{{ file.new_name }}'>
        </div>
        {% endfor %}
    </div>
    <button type='submit'>Rename Files</button>
</form>

{% if messages %}
<ul class='messages'>
    {% for message in messages %}
    <li{% if message.tags %} class='{{ message.tags }}'{% endif %}>{{ message }}</li>
    {% endfor %}
</ul>
{% endif %}