import os
import zipfile
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Zip the entire Django project'

    def handle(self, *args, **kwargs):
        project_dir = settings.BASE_DIR
        zip_filename = os.path.join(project_dir, 'django_project.zip')

        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for root, dirs, files in os.walk(project_dir):
                # Exclude the virtual environment directory, the zip file itself, and other unnecessary files
                if 'venv' in dirs:
                    dirs.remove('venv')
                if '__pycache__' in dirs:
                    dirs.remove('__pycache__')
                if 'django_project.zip' in files:
                    files.remove('django_project.zip')

                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, project_dir))

        self.stdout.write(self.style.SUCCESS(f'Django project zipped successfully into {zip_filename}'))
