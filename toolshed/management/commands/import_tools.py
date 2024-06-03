import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from toolshed.models import Tool

class Command(BaseCommand):
    help = 'Import tools from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                custodian_username = row['Custodian']
                custodian, created = User.objects.get_or_create(username=custodian_username)

                tool, created = Tool.objects.update_or_create(
                    name=row['Tool'],
                    defaults={
                        'tool_type': row['Type'],
                        'battery': row['Battery'] if row['Battery'] != 'NaN' else None,
                        'custodian': custodian,
                        'location': row['Location'],
                        'is_checked_out': row['Checkout'].lower() == 'true'
                    }
                )
                self.stdout.write(self.style.SUCCESS(f"Processed tool: {tool.name}"))

        self.stdout.write(self.style.SUCCESS('Successfully imported tools from CSV file'))
