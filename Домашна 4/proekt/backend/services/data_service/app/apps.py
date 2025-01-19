from django.apps import AppConfig


class DataServiceAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.services.data_service.app'
    label = 'data_service_app'  # Ensure this is unique
