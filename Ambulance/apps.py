from django.apps import AppConfig


class AmbulanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Ambulance'

    def ready(self) -> None:
        import Ambulance.signals  # noqa: F401
