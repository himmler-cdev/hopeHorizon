import csv
import os
from django.core.management.base import BaseCommand, CommandError
from backend import models
from django.db import migrations
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    '''
    Imports our our quotes.
    '''
    help = 'Imports our our quotes.'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='The name of the CSV file to process')

    def handle(self, *args, **options):
        filename = options['filename']
        
        # Check if the file exists
        if not os.path.isfile(filename):
            raise CommandError(f'The file "{filename}" does not exist.')

        # Open the file
        with open(filename, encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                models.Quote.objects.update_or_create(
                    quote=row['quote'],
                    author=row['author'],
                )


        