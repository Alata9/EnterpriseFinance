import os

from django.apps import AppConfig


class DirectoryappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "directory"

    # def ready(self):
    #     if os.environ.get('RUN_MAIN', None) != 'true':
    #         return

