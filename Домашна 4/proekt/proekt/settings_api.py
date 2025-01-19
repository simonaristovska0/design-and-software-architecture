from .settings import *  # Import everything from the main settings file

# Additional settings specific to the API service
INSTALLED_APPS = [
    'rest_framework',  # Include only necessary apps for the API
    'backend.services.data_service.app'
]

ROOT_URLCONF = 'backend.services.data_service.app.urls'  # Point to the API-specific URL configuration
