# 代码生成时间: 2025-09-01 02:10:27
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.core.management import call_command
from django.contrib.auth.decorators import login_required
import json
from django.db import transaction
from django.conf import settings
from datetime import datetime
import os
import shutil
import logging

# Set up logging
logger = logging.getLogger(__name__)

class BackupDatabaseView(View):
    """
    A view to handle database backup.

    This view triggers a database backup process.
    """
    def post(self, request, *args, **kwargs):
        try:
            # Trigger the backup process
            call_command('dumpdata', output=f"{settings.BASE_DIR}/backup/{datetime.now().isoformat()}.json")
            return JsonResponse({'message': 'Backup initiated successfully.'})
        except Exception as e:
            logger.error(f'Failed to initiate backup: {e}')
            return JsonResponse({'error': str(e)}, status=500)

class RestoreDatabaseView(View):
    """
    A view to handle database restore.

    This view triggers a database restore process.
    """
    def post(self, request, *args, **kwargs):
        try:
            backup_file = request.POST.get('backup_file')
            if not backup_file:
                return JsonResponse({'error': 'Backup file not provided.'}, status=400)

            backup_path = os.path.join(settings.BASE_DIR, 'backup', backup_file)
            if not os.path.exists(backup_path):
                return JsonResponse({'error': 'Backup file not found.'}, status=404)

            # Trigger the restore process
            with transaction.atomic():
                call_command('loaddata', backup_path)
            return JsonResponse({'message': 'Restore initiated successfully.'})
        except Exception as e:
            logger.error(f'Failed to initiate restore: {e}')
            return JsonResponse({'error': str(e)}, status=500)

# Define the URL patterns
urlpatterns = [
    path('backup/', login_required(BackupDatabaseView.as_view()), name='backup'),
    path('restore/', login_required(RestoreDatabaseView.as_view()), name='restore'),
]

# Note:
#   - The `login_required` decorator ensures that only authenticated users can access these views.
#   - The `dumpdata` and `loaddata` commands are used to backup and restore the database.
#   - The `transaction.atomic()` decorator ensures that the restore process is atomic,
#     meaning it either completes fully or not at all, to maintain data consistency.
#   - Proper error handling is implemented to ensure that any issues are logged and
#     the user is informed of the error.
#   - The `settings.BASE_DIR` is used to get the base directory of the project where
#     backups will be stored.
#   - The `datetime.now().isoformat()` generates a timestamp for the backup file.
