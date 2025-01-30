import csv
import os
from django.core.management.base import BaseCommand, CommandError
from backend import models

class Command(BaseCommand):
    '''
    Imports IMDB CSV sample file. Existing rows will be updated.
    '''
    help = 'Imports IMDB CSV sample file. Existing rows will be updated.'

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
                print(row)
                models.Quote.objects.update_or_create(
                    quote=row['quote'],
                    author=row['author'],
                )       

