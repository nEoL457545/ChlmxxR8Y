# 代码生成时间: 2025-09-16 08:12:32
from django.contrib.auth.models import User
from django.views.generic import View
from django.utils.timezone import now
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.conf import settings
from django.db import connections
from django.db.utils import DEFAULT_DB_ALIAS
from django.core.management import call_command
import json
import logging
import shutil
from datetime import datetime
import os
import zipfile
import tempfile

# 定义日志记录器
logger = logging.getLogger(__name__)

class BackupRestoreView(View):
    """
    用于数据备份和恢复的视图
    """
    def post(self, request):
        """
        处理POST请求，执行数据备份或恢复操作
        """
        action = request.POST.get('action')
        if action not in ['backup', 'restore']:
            return JsonResponse({'error': 'Invalid action'}, status=400)

        try:
            if action == 'backup':
                return self.backup_data()
            elif action == 'restore':
                return self.restore_data(request.FILES.get('backup_file'))
        except Exception as e:
            logger.error(f'Error during {action}: {e}')
            return JsonResponse({'error': str(e)}, status=500)

    def backup_data(self):
        """
        备份数据库数据
        """
        backup_file_path = tempfile.mkstemp(suffix='.zip')[1]
        call_command('dumpdata', output=backup_file_path)
        with zipfile.ZipFile(backup_file_path, 'w') as zipf:
            zipf.write(backup_file_path.replace('.zip', '.json'))
        os.remove(backup_file_path.replace('.zip', '.json'))

        with open(backup_file_path, 'rb') as f:
            response = HttpResponse(f, content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename=backup-{datetime.now().strftime("%Y%m%d%H%M%S")}.zip'
            return response

    def restore_data(self, backup_file):
        """
        从提供的备份文件恢复数据
        """
        if not backup_file or not backup_file.name.endswith('.zip'):
            return JsonResponse({'error': 'Invalid backup file'}, status=400)

        with tempfile.NamedTemporaryFile(suffix='.zip') as temp_file:
            shutil.copyfileobj(backup_file, temp_file)
            temp_file.flush()
            call_command('loaddata', temp_file.name)
            return JsonResponse({'message': 'Data restored successfully'})


# 在urls.py中添加以下路由
# from . import views
# urlpatterns = [
#     path('backup_restore/', views.BackupRestoreView.as_view(), name='backup_restore'),
# ]

# 在models.py中无需添加额外的模型，因为该应用利用Django自带的模型和命令
