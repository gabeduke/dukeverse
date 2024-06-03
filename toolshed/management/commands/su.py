import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        # Create superuser if it doesn't exist
        if not User.objects.filter(username=os.environ.get('SUPERUSER_USERNAME', 'admin')).exists():
            User.objects.create_superuser(
                os.environ.get('SUPERUSER_USERNAME', 'admin'),
                os.environ.get('SUPERUSER_EMAIL', 'admin@example.com'),
                os.environ.get('SUPERUSER_PASSWORD', 'password')
            )
            self.stdout.write(self.style.SUCCESS('Superuser created.'))
