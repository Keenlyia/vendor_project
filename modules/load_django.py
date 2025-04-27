import os
import sys

import django

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'vendr_project'))
sys.path.append(project_path)

os.environ["DJANGO_SETTINGS_MODULE"] = "vendr_project.settings"
django.setup()