import os
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proekt.settings')  # Adjust this based on your setup

if __name__ == "__main__":
    execute_from_command_line()