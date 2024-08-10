from django.apps import AppConfig


class CrewConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Crew'
    
    def ready(self):
        import Crew.signals  # noqa: F401
