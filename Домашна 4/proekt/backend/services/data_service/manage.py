import os
import sys

# Add the project root directory to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proekt.settings')

from django.core.management import execute_from_command_line

if __name__ == "__main__":
    execute_from_command_line()