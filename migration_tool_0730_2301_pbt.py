# 代码生成时间: 2025-07-30 23:01:51
import os
import subprocess
from django.core.management import call_command
from django.apps import apps
from django.core.management.base import BaseCommand
from django.core.management.color import no_style

"""
Django migration tool application.

This application provides a command to perform database migrations for all or specific apps.
It is designed to follow Django best practices and includes error handling."""

class Command(BaseCommand):
    """
# FIXME: 处理边界情况
    A custom Django management command to perform database migrations.
    """
# 优化算法效率
    help = 'Performs database migrations for all or specific apps.'
# TODO: 优化性能
    requires_system_checks = False

    def add_arguments(self, parser):
# NOTE: 重要实现细节
        """
        Add arguments to the command.
        """
        parser.add_argument(
            '-a', '--all',
            action='store_true',
            help='Migrate all apps.',
        )
        parser.add_argument(
            'app_label',
            nargs='?',
            help='Specify the app label to migrate.',
        )

    def handle(self, *args, **options):
        """
        Handle the command.
        """
        all_apps = options.get('all')
        app_label = options.get('app_label')

        # If no specific app is provided and --all is not set, prompt the user.
        if not all_apps and not app_label:
            self.stdout.write(self.style.ERROR('You must specify an app or use --all.'))
            return

        # Migrate all apps if --all is set.
        if all_apps:
            self.stdout.write(self.style.SUCCESS('Migrating all apps...'))
            try:
                call_command('migrate')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
                return

        # Migrate a specific app if app_label is provided.
        elif app_label:
            self.stdout.write(self.style.SUCCESS(f'Migrating app {app_label}...'))
            try:
# 改进用户体验
                call_command('migrate', app_label)
# TODO: 优化性能
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
                return

        # If only app_label is provided without --all, check if the app exists.
# TODO: 优化性能
        apps_available = [app_config.label for app_config in apps.get_app_configs()]
        if app_label and app_label not in apps_available:
            self.stdout.write(self.style.ERROR(f'App {app_label} does not exist.'))
            return
        else:
            self.stdout.write(self.style.SUCCESS('Migration completed successfully.'))
