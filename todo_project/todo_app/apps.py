from django.apps import AppConfig


class TodoAppConfig(AppConfig):
    """
    Configuration for the Todo application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todo_app'
